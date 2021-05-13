# -*- coding: utf-8 -*-

from . import f2_nc

from . import nnlo


class NonSinglet(f2_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        def reg(z):
            return nnlo.xc2ns2p.c2nc2a(z, self.nf)

        def sing(z):
            return nnlo.xc2ns2p.c2ns2b(z, self.nf)

        def loc(x):
            return nnlo.xc2ns2p.c2nc2c(x, self.nf)

        return reg, sing, loc


class Gluon(f2_nc.Gluon):
    pass


class Singlet(f2_nc.Singlet):
    pass
