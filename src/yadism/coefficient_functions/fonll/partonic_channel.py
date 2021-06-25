# -*- coding: utf-8 -*-
import numpy as np
from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..partonic_channel import RSL


class PartonicChannelAsy(pc.PartonicChannel):
    def __init__(self, *args, mu2hq):
        super().__init__(*args)
        self.L = np.log(self.ESF.Q2 / mu2hq)


class PartonicChannelAsyIntrinsic(pc.PartonicChannel):
    def __init__(self, *args, m1sq, m2sq):
        super().__init__(*args)
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


class FMatching(PartonicChannelAsyIntrinsic):
    ffns = lambda *_args, m1sq, m2sq: None

    def __init__(self, *args, m1sq, m2sq, mu2hq):
        super().__init__(*args, m1sq=m1sq, m2sq=m2sq)
        self.l = np.log(self.Q2 / mu2hq)

    def obj(self):
        return self.ffns(self.ESF, self.nf, m1sq=self.m1sq, m2sq=self.m2sq)

    def parent_lo_local(self):
        parent_LO = self.obj().LO()
        if parent_LO is None:
            return None
        return parent_LO.args["loc"][0]


class FMatchingQuark(FMatching):
    def NLO(self):
        icl = self.parent_lo_local()
        if icl is None:
            return None
        asnorm = 2.0
        l = self.l

        def sing(z, _args):
            # this coefficient function is *almost* proportional to P_qq
            # i.e. 2CF * (1.0 + z ** 2) / (1.0 - z) is the "bare" P_qq
            return (
                asnorm
                * icl
                * constants.CF
                * ((1.0 + z ** 2) / (1.0 - z) * (l - 2.0 * np.log(1.0 - z) - 1.0))
            )

        # MMa:
        # FortranForm@FullSimplify@Integrate[(1 + z^2)/(1 - z) (l - 2 Log[1 - z] - 1), {z, 0, x}, Assumptions -> {0 < x < 1}] # pylint: disable=line-too-long
        def loc(x, _args):
            return (
                -asnorm
                * icl
                * constants.CF
                * (
                    -(x * (4.0 + l * (2.0 + x))) / 2.0
                    + np.log(1.0 - x)
                    * (-1.0 - 2.0 * l + x * (2.0 + x) + 2.0 * np.log(1.0 - x))
                )
            )

        return RSL(sing=sing, loc=loc)


class FMatchingCC(FMatching):
    ffns = lambda *_args, m1sq: None

    def __init__(self, *args, m1sq, mu2hq):
        super().__init__(*args, m1sq=m1sq, m2sq=0.0, mu2hq=mu2hq)

    def obj(self):
        return self.ffns(self.ESF, self.nf, m1sq=self.m1sq)


class FMatchingQuarkCC(FMatchingCC, FMatchingQuark):
    pass


class FMatchingGluon(FMatching):
    def NLO(self):
        return self.mk_nlo_raw(self.l)

    def mk_nlo_raw(self, l):
        icl = self.parent_lo_local()
        if icl is None:
            return None

        # since as and p_qg appear together there is no need to put an explicit as_norm here
        def reg(z, _args):
            return icl * split.lo.pqg_single(z, np.array([], dtype=float)) * l

        return RSL(reg)


class FMatchingGluonCC(FMatchingCC, FMatchingGluon):
    pass
