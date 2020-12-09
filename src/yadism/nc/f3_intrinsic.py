# -*- coding: utf-8 -*-

from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F3IntrinsicRp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.ESF.x / self.convolution_point()
        return 0, 0, factor
