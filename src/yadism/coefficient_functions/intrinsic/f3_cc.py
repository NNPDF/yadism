import numpy as np
from eko import constants

from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_cc


class Rplus(pc.ChargedCurrentBase):
    def __init__(self, *args, m1sq):
        super().__init__(*args, m1sq=m1sq)
        self.lo = 1.0

    def LO(self):
        return RSL.from_delta(self.lo)

    def NLO(self):
        norm = constants.CF
        lnomx = raw_cc.lnomx * norm * self.lo
        omx = raw_cc.omx(self.y) * norm * self.lo
        delta = raw_cc.f3sv(self.y) * norm

        def reg(z, _args):
            return norm * raw_cc.f3r(self.y, z) - (lnomx * np.log(1.0 - z) + omx) / (
                1.0 - z
            )

        return RSL.from_distr_coeffs(reg, (delta, omx, lnomx))
