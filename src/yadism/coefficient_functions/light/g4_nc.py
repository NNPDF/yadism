from ..partonic_channel import RSL
from . import nlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """|ref| Eq. (4) of :cite:`Borsa:2022irn`."""
        # leading order is just a delta function
        return RSL.from_delta(1.0)

    @staticmethod
    def NLO():
        """|ref| Eq. (19) of :cite:`Borsa:2022irn`."""
        return RSL.from_distr_coeffs(
            nlo.g4.ns_reg, (nlo.g4.ns_delta, nlo.g4.ns_omx, nlo.g4.ns_logomx)
        )

    def NNLO(self):
        return None


class Gluon(pc.LightBase):
    def NLO(self):
        return None

    def NNLO(self):
        return None


class Singlet(pc.LightBase):
    def NNLO(self):
        return None
