# -*- coding: utf-8 -*-
import numpy as np

from eko import constants

from .. import splitting_functions as split
from .. import partonic_channel as pc
from ..partonic_channel import RSL


class PartonicChannelAsy(pc.PartonicChannel):
    def __init__(self, esf, mu2hq):
        super().__init__(esf)
        self.L = np.log(esf.Q2 / mu2hq)


class PartonicChannelAsyIntrinsic(pc.PartonicChannel):
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


class FMatching(PartonicChannelAsyIntrinsic):
    ffns = lambda *_args: None

    def __init__(self, ESF, m1sq, m2sq, mu2hq):
        super().__init__(ESF, m1sq, m2sq)
        self.l = np.log(self.Q2 / mu2hq)


class FMatchingQuark(FMatching):
    def NLO(self):
        obj = self.ffns(self.ESF, self.m1sq, self.m2sq)
        parent_LO = obj.LO()
        try:
            icl = parent_LO.args["loc"][0]
        except KeyError:  # is there a local part in the parent?
            return parent_LO  # no, so it should be 0 and we can pass through
        asnorm = 2.0
        l = self.l

        def sing(z, args):
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
        def loc(x, args):
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

    def NLO_fact(self):
        obj = self.ffns(self.ESF, self.m1sq, self.m2sq)
        parent_LO = obj.LO()
        try:
            _, _, icl = parent_LO
        except TypeError:
            return parent_LO

        def reg(z):
            return -icl * split.pqq_reg(z)

        def sing(z):
            return -icl * split.pqq_sing(z)

        def local(x):
            return -icl * split.pqq_local(x)

        return reg, sing, local


class FMatchingGluon(FMatching):
    def NLO(self):
        return self.mk_nlo_raw(self.l)

    def mk_nlo_raw(self, l):
        obj = self.ffns(self.ESF, self.m1sq, self.m2sq)
        parent_LO = obj.LO()
        try:
            icl = parent_LO.args["loc"][0]
        except KeyError:  # is there a local part in the parent?
            return parent_LO  # no, so it should be 0 and we can pass through

        # since as and p_qg appear together there is no need to put an explicit as_norm here
        # the explicit 2 instead is coming from Eq. (B.25) of :cite:`luca-intrinsic`.
        def reg(z, args):
            return icl * 2.0 * split.pqg(z) * l

        return RSL(reg)

    def NLO_fact(self):
        return self.mk_nlo_raw(-1.0)
