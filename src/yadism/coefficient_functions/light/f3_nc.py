"""
See :mod:`f3_cc` docstring for the name conventions.
"""
from .. import partonic_channel as pc
from ..partonic_channel import RSL
from . import f2_nc, n3lo, nlo, nnlo


class NonSinglet(f2_nc.NonSinglet):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`155`, :cite:`moch-f3nc`.
        """

        return RSL.from_distr_coeffs(
            nlo.f3.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """
        |ref| implements the sum between :eqref:`2.8` and :eqref:`3.5`, :cite:`Davies:2016ruz`
        or :eqref:`208`, :cite:`moch-f3nc`.
        """

        return RSL(
            nnlo.xc3ns2p.c3np2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3np2c, [self.nf]
        )

    def N3LO(self):
        """
        |ref| implements the sum between :eqref:`2.11` and :eqref:`3.8`, :cite:`Davies:2016ruz`.
        """

        return RSL(
            n3lo.xc3ns3p.c3np3a,
            n3lo.xc3ns3p.c3ns3b,
            n3lo.xc3ns3p.c3np3c,
            [self.nf, False],
        )


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
