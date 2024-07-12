"""See :mod:`f3_cc` docstring for the name conventions."""

from .. import partonic_channel as epc
from ..partonic_channel import RSL
from . import f2_nc, n3lo, nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(f2_nc.NonSinglet):
    @staticmethod
    def NLO():
        """|ref| implements :eqref:`155`, :cite:`moch-f3nc`."""

        return RSL.from_distr_coeffs(
            nlo.f3.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """|ref| implements :eqref:`3.6` :cite:`vogt-f3cc`, or :eqref:`208`, :cite:`moch-f3nc`, or :eqref:`2.8` :cite:`Davies:2016ruz`."""

        return RSL(
            nnlo.xc3ns2p.c3nm2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3nm2c, [self.nf]
        )

    def N3LO(self):
        """|ref| implements :eqref:`3.7` :cite:`vogt-f3cc`, or :eqref:`2.11` :cite:`Davies:2016ruz`."""
        return RSL(
            n3lo.xc3ns3p.c3nm3a,
            n3lo.xc3ns3p.c3ns3b,
            n3lo.xc3ns3p.c3nm3c,
            [self.nf],
        )


class Gluon(epc.EmptyPartonicChannel):
    pass


class Singlet(epc.EmptyPartonicChannel):
    pass


class Valence(pc.LightBase):

    def N3LO(self):
        """Part proportional to :math:`fl_{02}` of :eqref:`2.11` :cite:`Davies:2016ruz`."""

        return RSL(
            n3lo.xc3ns3p.c3nsv3a,
            args=[self.nf],
        )
