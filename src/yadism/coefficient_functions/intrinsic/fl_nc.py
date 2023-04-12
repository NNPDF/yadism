# -*- coding: utf-8 -*-
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc


class Splus(pc.NeutralCurrentBase):
    def LO(self):
        factor = (self.delta / self.ESF.Q2 - self.sigma_pp / self.delta) * self.eta
        return RSL.from_delta(factor)

    def NLO(self):
        return self.mkNLO("l", "splus")


class Sminus(pc.NeutralCurrentBase):
    def LO(self):
        factor = 2.0 * np.sqrt(self.m1sq * self.m2sq) / self.delta * self.eta
        return RSL.from_delta(factor)

    def NLO(self):
        return self.mkNLO("l", "sminus")
