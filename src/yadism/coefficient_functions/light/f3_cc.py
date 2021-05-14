# -*- coding: utf-8 -*-
import numpy as np

from ..partonic_channel import RSL
from .. import partonic_channel as pc
from . import f3_nc

from . import nnlo


class NonSinglet(f3_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xc3ns2p.c3nm2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3nm2c, [self.nf]
        )


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
