# -*- coding: utf-8 -*-

import numba as nb

from ..intrinsic import fl_nc as intrinsic
from ..light import fl_nc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLO(z, _args):
    return raw_nc.clg1am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NNLO(z, args):
    L = args[0]
    return (raw_nc.clg2am0_aq(z) - raw_nc.clg2am0_af(z)) * L + raw_nc.clg2am0_a0(z)


class AsyGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_NNLO, args=[self.L])


class AsyGluonAA(AsyGluonVV):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NNLO(z, args):
    L = args[0]
    return (raw_nc.clps2am0_aq(z) - raw_nc.clps2am0_af(z)) * L + raw_nc.clps2am0_a0(z)


class AsySingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NNLO, args=[self.L])


class AsySingletAA(AsySingletVV):
    pass


class PdfMatchingNonSinglet(EmptyPartonicChannel):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


# @nb.njit("f8(f8,f8[:])", cache=True)
# def cns_NNLO(z, args):
#     L = args[0]
#     return raw_nc.clns2am0_aq(z) * L + raw_nc.clns2am0_a0(z)


# class AsyNonSingletMissing(pc.PartonicChannelAsy):
#     def NNLO(self):
#         return RSL(cns_NNLO, args=[self.L])


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = intrinsic.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = intrinsic.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = intrinsic.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = intrinsic.Sminus
