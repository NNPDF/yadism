# -*- coding: utf-8 -*-
from ..partonic_channel import RSL
from . import f2_nc, nnlo


class NonSingletEven(f2_nc.NonSinglet):
    pass


class Gluon(f2_nc.Gluon):
    pass


class Singlet(f2_nc.Singlet):
    pass


class NonSingletOdd(f2_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xc2ns2p.c2nc2a, nnlo.xc2ns2p.c2ns2b, nnlo.xc2ns2p.c2nc2c, [self.nf]
        )
