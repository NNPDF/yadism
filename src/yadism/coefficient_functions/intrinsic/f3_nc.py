# -*- coding: utf-8 -*-

from . import partonic_channel as pc
from ..partonic_channel import RSL


class Rplus(pc.NeutralCurrentBase):
    def LO(self):
        factor = self.ESF.x / self.convolution_point()
        return RSL.from_delta(factor)

    def NLO(self):
        return self.mkNLO("3", "rplus")


class Rminus(pc.NeutralCurrentBase):
    def NLO(self):
        return self.mkNLO("3", "rminus")
