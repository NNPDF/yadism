# -*- coding: utf-8 -*-
from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F2IntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.eta
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("f2", "splus", self.x * self.delta / self.Q2)


class F2IntrinsicSm(PartonicChannelHeavyIntrinsic):
    def NLO(self):
        return self.mkNLO("f2", "sminus", 0)
