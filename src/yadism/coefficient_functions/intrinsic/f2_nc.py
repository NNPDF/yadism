from ..partonic_channel import RSL
from . import partonic_channel as pc


class Splus(pc.NeutralCurrentBase):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.eta
        return RSL.from_delta(factor)

    def NLO(self):
        return self.mkNLO("2", "splus")


class Sminus(pc.NeutralCurrentBase):
    def NLO(self):
        return self.mkNLO("2", "sminus")
