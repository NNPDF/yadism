# -*- coding: utf-8 -*-
from eko import constants

from . import partonic_channel as pc
from ..partonic_channel import RSL


class AsyQuark(pc.PartonicChannelAsy):
    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z, args):
            return CF * 2.0 * z * as_norm

        return RSL(reg)


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z, args):
            return 4.0 * z * (1.0 - z) * as_norm

        return RSL(reg)
