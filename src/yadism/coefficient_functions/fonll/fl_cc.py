# -*- coding: utf-8 -*-
from eko import constants

from . import partonic_channel as pc
from ..partonic_channel import RSL
from ..intrinsic import fl_cc


class AsyQuark(pc.PartonicChannelAsy):
    # TODO inherit from light
    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z, _args):
            return CF * 2.0 * z * as_norm

        return RSL(reg)


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z, _args):
            return 4.0 * z * (1.0 - z) * as_norm

        return RSL(reg)


class MatchingIntrinsicSplus(pc.FMatchingQuarkCC):
    ffns = fl_cc.Splus


class MatchingGluonSplus(pc.FMatchingGluonCC):
    ffns = fl_cc.Splus
