# -*- coding: utf-8 -*-

from eko import constants

from . import partonic_channel as pc
from ..partonic_channel import RSL
from ..intrinsic import fl_nc


class AsyGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        def cg(z, args):
            return constants.TR * (16 * z * (1 - z))

        return RSL(cg)


class AsyGluonAA(AsyGluonVV):
    pass


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = fl_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = fl_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = fl_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = fl_nc.Sminus
