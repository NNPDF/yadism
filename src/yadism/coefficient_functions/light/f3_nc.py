# -*- coding: utf-8 -*-
from eko import constants

from . import f2_nc
from .. import partonic_channel as pc

from . import nnlo


class NonSinglet(f2_nc.NonSinglet):
    def NLO(self):
        """
        |ref| implements :eqref:`155`, :cite:`moch-f3nc`.
        """
        CF = constants.CF

        reg_f2, sing, loc = super().NLO()

        def reg(z, CF=CF):
            return reg_f2(z) - 2 * CF * (1 + z)

        return reg, sing, loc

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        def reg(z):
            return nnlo.xc3ns2p.c3np2a(z, self.nf)

        def sing(z):
            return nnlo.xc3ns2p.c3ns2b(z, self.nf)

        def loc(x):
            return nnlo.xc3ns2p.c3np2c(x, self.nf)

        return reg, sing, loc


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
