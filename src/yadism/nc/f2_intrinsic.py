# -*- coding: utf-8 -*-
from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F2IntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.ESF.x / self.convolution_point()
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("f2", "splus")


class F2IntrinsicSm(PartonicChannelHeavyIntrinsic):
    def NLO(self):
        return self.mkNLO("f2", "sminus")
