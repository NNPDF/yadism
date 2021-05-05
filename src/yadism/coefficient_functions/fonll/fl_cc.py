# -*- coding: utf-8 -*-
from eko import constants

from . import partonic_channel as pc


class AsyQuark(pc.PartonicChannelAsy):
    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z):
            return CF * 2.0 * z * as_norm

        return reg


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z):
            return 4.0 * z * (1.0 - z) * as_norm

        return reg
