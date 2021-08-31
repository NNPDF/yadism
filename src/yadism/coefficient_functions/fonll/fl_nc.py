# -*- coding: utf-8 -*-

import numba as nb

from ..intrinsic import fl_nc
from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NNLO(z, args):
    L = args[0]
    return raw_nc.clg2am0_aq(z) * L + raw_nc.clg2am0_a0(z)


class AsyGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(raw_nc.clg1am0_a0)

    def NNLO(self):
        return RSL(cg_NNLO, args=[self.L])


class AsyGluonAA(AsyGluonVV):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NNLO(z, args):
    L = args[0]
    return raw_nc.clps2am0_aq(z) * L + raw_nc.clps2am0_a0(z)


class AsySingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NNLO, args=[self.L])


class AsySingletAA(AsySingletVV):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLO(z, args):
    L = args[0]
    return raw_nc.clns2am0_a0(z) * L + raw_nc.clns2am0_a0(z)


class AsyNonSingletMissing(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NNLO, args=[self.L])


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = fl_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = fl_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = fl_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = fl_nc.Sminus
