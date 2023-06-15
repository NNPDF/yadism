"""
Note that at |N3LO| the source files in fortran follow :cite:`vogt-f3cc` notation
where the odd-N moments are called minus even if they correspond to :math:`\nu + \bar{\nu}`.
This convention is changed in :cite:`Davies:2016ruz` where the |N3LO| CC results are presented
for the first time. Referred equations are not always in agreement with the code conventions.
"""
from .. import partonic_channel as pc
from ..partonic_channel import RSL
from . import f3_nc, n3lo, nnlo


class NonSingletOdd(f3_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`3.6`, :cite:`vogt-f3cc`
        or :eqref:`2.8`, :cite:`Davies:2016ruz`.
        """

        return RSL(
            nnlo.xc3ns2p.c3nm2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3nm2c, [self.nf]
        )

    def N3LO(self):
        """
        |ref| implements :eqref:`3.7`, :cite:`vogt-f3cc` or :eqref:`2.11`, :cite:`Davies:2016ruz`.
        """

        return RSL(
            n3lo.xc3ns3p.c3nm3a,
            n3lo.xc3ns3p.c3ns3b,
            n3lo.xc3ns3p.c3nm3c,
            [self.nf, True],
        )


class NonSingletEven(f3_nc.NonSinglet):
    pass


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
