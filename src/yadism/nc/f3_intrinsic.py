# -*- coding: utf-8 -*-

from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F3IntrinsicRp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.ESF.x / self.convolution_point()
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("f3", "rplus")


class F3IntrinsicRm(PartonicChannelHeavyIntrinsic):
    def NLO(self):
        return self.mkNLO("f3", "rminus")
