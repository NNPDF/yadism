from ..partonic_channel import RSL
from . import nlo, nnlo
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
            nlo.f2.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """|ref| Eq. (19) of :cite:`Borsa:2022irn`."""
        return RSL(
            nnlo.xc2ns2p.c2nn2a, nnlo.xc2ns2p.c2ns2b, nnlo.xc2ns2p.c2nn2c, [self.nf]
        )


class Gluon(pc.LightBase):
    def NLO(self):
        return None

    def NNLO(self):
        return None


class Singlet(pc.LightBase):
    def NNLO(self):
        return None
