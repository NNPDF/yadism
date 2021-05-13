# -*- coding: utf-8 -*-

from . import fl_nc

from . import nnlo


class NonSinglet(fl_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        def reg(z):
            return nnlo.xclns2p.clnc2a(z, self.nf)

        def loc(x):
            return nnlo.xclns2p.clnc2c(x)

        return reg, 0.0, loc


class Gluon(fl_nc.Gluon):
    pass


class Singlet(fl_nc.Singlet):
    pass
