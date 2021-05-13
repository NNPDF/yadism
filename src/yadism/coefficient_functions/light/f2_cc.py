# -*- coding: utf-8 -*-
import numpy as np

from . import f2_nc

from . import nnlo


class NonSinglet(f2_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        def reg(z):
            return nnlo.xc2ns2p.c2nc2a(z, np.array([self.nf], dtype=float))

        def sing(z):
            return nnlo.xc2ns2p.c2ns2b(z, np.array([self.nf], dtype=float))

        def loc(x):
            return nnlo.xc2ns2p.c2nc2c(x, np.array([self.nf], dtype=float))

        return reg, sing, loc


class Gluon(f2_nc.Gluon):
    pass


class Singlet(f2_nc.Singlet):
    pass
