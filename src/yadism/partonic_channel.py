# -*- coding: utf-8 -*-

import numpy as np

from eko import constants

from . import ic

from .esf.distribution_vec import rsl_from_distr_coeffs
from . import splitting_functions as split


class PartonicChannel(dict):
    """
    Container of partonic coefficient functions

    Parameters
    ----------
        ESF : yadism.structure_function.esf.EvaluatedStructureFunction
            parent ESF
    """

    def __init__(self, ESF):
        super().__init__()
        self.ESF = ESF
        # default coeff functions to 0
        self[(0, 0, 0, 0)] = self.decorator(self.LO)
        self[(1, 0, 0, 0)] = self.decorator(self.NLO)
        self[(1, 0, 0, 1)] = self.decorator(self.NLO_fact)

    def convolution_point(self):
        """
        Convolution point
        """
        return self.ESF.x  # pylint: disable=protected-access

    def decorator(self, f):
        """
        Deactivate preprocessing

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        return f

    @staticmethod
    def LO():
        return None

    @staticmethod
    def NLO():
        return None

    @staticmethod
    def NLO_fact():
        return None


class EmptyPartonicChannel(PartonicChannel):
    def __init__(self, *args, **_kwargs):
        super().__init__(*args)


class PartonicChannelLight(PartonicChannel):
    def __init__(self, *args, nf):
        super().__init__(*args)
        self.nf = nf


class PartonicChannelAsy(PartonicChannel):
    def __init__(self, esf, mu2hq):
        super().__init__(esf)
        self.L = np.log(esf.Q2 / mu2hq)


class PartonicChannelAsyIntrinsic(PartonicChannel):
    def __init__(self, ESF, m1sq, m2sq):
        super().__init__(ESF)
        self.Q2 = self.ESF.Q2
        self.x = self.ESF.x
        self.m1sq = m1sq
        self.m2sq = m2sq
        self.sigma_pm = self.Q2 + self.m2sq - self.m1sq
        self.delta = self.kinematic_delta(self.m1sq, self.m2sq, -self.Q2)
        self.eta = 2.0 * self.Q2 / (self.sigma_pm + self.delta)

    @staticmethod
    def kinematic_delta(a, b, c):
        return np.sqrt(a ** 2 + b ** 2 + c ** 2 - 2 * (a * b + b * c + c * a))

    def convolution_point(self):
        return self.x / self.eta


class PartonicChannelHeavyIntrinsic(PartonicChannelAsyIntrinsic):
    def __init__(self, ESF, m1sq, m2sq):
        super().__init__(ESF, m1sq, m2sq)
        self.sigma_pp = self.Q2 + self.m2sq + self.m1sq
        self.sigma_mp = self.Q2 - self.m2sq + self.m1sq

    def init_nlo_vars(self):
        self.I1 = ic.I1(self)
        self.Cplus = ic.Cplus(self)
        self.C1m = ic.C1m(self)
        self.C1p = ic.C1p(self)
        self.CRm = ic.CRm(self)
        self.S = ic.S(self)
        self.L_xisoft = np.log(
            (self.sigma_pp - self.delta) / (self.sigma_pp + self.delta)
        )

    def init_vars(self, z):
        self.s1hat = (
            (1.0 - z)
            * ((self.delta - self.sigma_pm) * z + self.delta + self.sigma_pm)
            / 2.0
            / z
        )
        self.deltap = self.kinematic_delta(self.m1sq, self.s1hat + self.m2sq, -self.Q2)
        self.L_xi = np.log(
            (self.sigma_pp + self.s1hat - self.deltap)
            / (self.sigma_pp + self.s1hat + self.deltap)
        )

    def mkNLO(self, kind, RS):
        self.init_nlo_vars()
        norm = 2.0 * constants.CF * self.eta / self.x  # 2 = as_norm
        omx = norm * ic.__getattribute__(  # pylint: disable=no-member
            f"f{kind}_{RS}_soft"
        )(self)

        delta = norm * (
            ic.__getattribute__(f"f{kind}_{RS}_virt")(self)  # pylint: disable=no-member
            + self.S  # add normalization between curly and upright F
            * ic.__getattribute__(f"m{kind}_{RS}")(self)  # pylint: disable=no-member
        )

        def reg(z):
            self.init_vars(z)
            return norm * ic.__getattribute__(  # pylint: disable=no-member
                f"f{kind}_{RS}_raw"
            )(self) - omx / (1.0 - z)

        return rsl_from_distr_coeffs(reg, delta, omx)


class FMatching(PartonicChannelAsyIntrinsic):
    def __init__(self, ESF, m1sq, m2sq, mu2hq):
        super().__init__(ESF, m1sq, m2sq)
        self.l = np.log(self.Q2 / mu2hq)


class FMatchingQuark(FMatching):
    def mk_nlo(self, intrinsic_pc):
        obj = intrinsic_pc(self.ESF, self.m1sq, self.m2sq)
        parent_LO = obj.LO()
        try:
            _, _, icl = parent_LO
        except TypeError:
            return parent_LO
        asnorm = 2.0
        l = self.l

        def sing(z):
            return (
                asnorm
                * icl
                * constants.CF
                * ((1.0 + z ** 2) / (1.0 - z) * (l - 2.0 * np.log(1.0 - z) - 1.0))
            )

        # MMa: FortranForm@FullSimplify@Integrate[(1 + z^2)/(1 - z) (l - 2 Log[1 - z] - 1), {z, 0, x}, Assumptions -> {0 < x < 1}]
        def loc(x):
            return (
                asnorm
                * icl
                * constants.CF
                * (
                    -(x * (4.0 + l * (2.0 + x))) / 2.0
                    + np.log(1.0 - x)
                    * (-1.0 - 2.0 * l + x * (2.0 + x) + 2.0 * np.log(1.0 - x))
                )
            )

        return 0, sing, loc
    # TODO add xiF via mk_nlo_fact


class FMatchingGluon(FMatching):
    def mk_nlo(self, intrinsic_pc):
        obj = intrinsic_pc(self.ESF, self.m1sq, self.m2sq)
        parent_LO = obj.LO()
        try:
            _, _, icl = parent_LO
        except TypeError: # is there a local part in the parent?
            return parent_LO # no, so it should be 0 and we can pass through
        l = self.l
        # since as and p_qg appear together there is no need to put an explicit as_norm here
        # the explicit 2 instead is coming from Eq. (B.25) of Lucas IC paper
        # TODO add proper cite
        def reg(z):
            return -icl * 2.0 * split.pqg(z) * l

        return reg, 0, 0
