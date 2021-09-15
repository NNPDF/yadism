# -*- coding: utf-8 -*-

import numba as nb

from ..intrinsic import f2_nc
from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLO(z, args):
    L = args[0]
    return L * raw_nc.c2g1am0_aq(z) + raw_nc.c2g1am0_a0(z)


class AsyGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_NLO, args=[self.L])


class AsyGluonAA(AsyGluonVV):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NNLO(z, args):
    L = args[0]
    return (
        raw_nc.c2ps2am0_aq2(z) * L ** 2
        + raw_nc.c2ps2am0_aq(z) * L
        + raw_nc.c2ps2am0_a0(z)
    )


class AsySingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NNLO, args=[self.L])


class AsySingletAA(AsySingletVV):
    pass


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = f2_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = f2_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = f2_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = f2_nc.Sminus
