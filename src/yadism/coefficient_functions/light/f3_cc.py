# -*- coding: utf-8 -*-
import numpy as np

from . import f3_nc
from .. import partonic_channel as pc

from . import nnlo


class NonSinglet(f3_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        def reg(z):
            return nnlo.xc3ns2p.c3nm2a(z, np.array([self.nf], dtype=float))

        def sing(z):
            return nnlo.xc3ns2p.c3ns2b(z, np.array([self.nf], dtype=float))

        def loc(x):
            return nnlo.xc3ns2p.c3nm2c(x, np.array([self.nf], dtype=float))

        return reg, sing, loc


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
