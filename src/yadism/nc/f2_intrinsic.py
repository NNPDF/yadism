# -*- coding: utf-8 -*-
from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F2IntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.eta
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("2", "splus")


class F2IntrinsicSm(PartonicChannelHeavyIntrinsic):
    def NLO(self):
        #  return 0.0
        return self.mkNLO("2", "sminus")
