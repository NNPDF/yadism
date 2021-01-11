# -*- coding: utf-8 -*-
import numpy as np
from ..partonic_channel import PartonicChannelHeavyIntrinsic


class FLIntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = (
            (self.delta / self.ESF.Q2 - self.sigma_pp / self.delta)
            * self.ESF.x
            / self.convolution_point()
        )
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("fl", "splus")


class FLIntrinsicSm(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = (
            2.0
            * np.sqrt(self.m1sq * self.m2sq)
            / self.delta
            * self.ESF.x
            / self.convolution_point()
        )
        return 0, 0, factor

    def NLO(self):
        return self.mkNLO("fl", "sminus")
