# -*- coding: utf-8 -*-
from .. import partonic_channel as pc
from ..partonic_channel import RSL
from . import f3_nc, nnlo


class NonSingletOdd(f3_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xc3ns2p.c3nm2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3nm2c, [self.nf]
        )


class NonSingletEven(f3_nc.NonSinglet):
    pass


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
