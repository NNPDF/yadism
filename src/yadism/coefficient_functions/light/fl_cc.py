# -*- coding: utf-8 -*-
from ..partonic_channel import RSL
from . import fl_nc, nnlo


class NonSingletEven(fl_nc.NonSinglet):
    pass


class Gluon(fl_nc.Gluon):
    pass


class Singlet(fl_nc.Singlet):
    pass


class NonSingletOdd(fl_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xclns2p.clnc2a, loc=nnlo.xclns2p.clnc2c, args=dict(reg=[self.nf])
        )
