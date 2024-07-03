"""
Note that the source files (given in fortran) follow the notations in :cite:`vogt-f3cc`
where the odd-N moments are called minus even if they correspond to :math:`\nu + \bar{\nu}`,
while even-N moments are called plus even if they correspond to :math:`\nu - \bar{\nu}`.
This convention is changed in :cite:`Davies:2016ruz` where the |N3LO| CC results are presented
for the first time.
"""

from .. import partonic_channel as pc
from ..partonic_channel import RSL
from . import f3_nc, n3lo, nnlo


class NonSingletOdd(f3_nc.NonSinglet):
    pass


class NonSingletEven(f3_nc.NonSinglet):
    def NNLO(self):
        """|ref| implements the sum between :eqref:`2.8` and :eqref:`3.5`, :cite:`Davies:2016ruz`."""
        return RSL(
            nnlo.xc3ns2p.c3np2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3np2c, [self.nf]
        )

    def N3LO(self):
        """|ref| implements the sum between :eqref:`2.11` and :eqref:`3.8`, :cite:`Davies:2016ruz`."""
        return RSL(
            n3lo.xc3ns3p.c3np3a,
            n3lo.xc3ns3p.c3ns3b,
            n3lo.xc3ns3p.c3np3c,
            [self.nf],
        )


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass


class Valence(f3_nc.Valence):
    pass
