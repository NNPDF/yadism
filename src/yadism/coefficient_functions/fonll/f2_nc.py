# -*- coding: utf-8 -*-

import numba as nb

from ..intrinsic import f2_nc as intrinsic
from ..light import f2_nc as light
from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_LL_NLO(z, args):
    L = args[0]
    return raw_nc.c2g1am0_aq(z) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_const_NLO(z, _args):
    return raw_nc.c2g1am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_LL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2g2am0_aq2(z) - raw_nc.c2g2am0_aqf(z)) * L ** 2


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLL_NNLO(z, args):
    L = args[0]
    return +(raw_nc.c2g2am0_aq(z) - raw_nc.c2g2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_const_NNLO(z, _args):
    return +raw_nc.c2g2am0_a0(z)


class AsyLLGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_LL_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_LL_NNLO, args=[self.L])


class AsyNLLGluonVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cg_NLL_NNLO, args=[self.L])


class AsyConstGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_const_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_const_NNLO)


class AsyLLGluonAA(AsyLLGluonVV):
    pass


class AsyNLLGluonAA(AsyNLLGluonVV):
    pass


class AsyConstGluonAA(AsyConstGluonVV):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_LL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2ps2am0_aq2(z) - raw_nc.c2ps2am0_aqf(z)) * L ** 2


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NLL_NNLO(z, args):
    L = args[0]
    return +(raw_nc.c2ps2am0_aq(z) - raw_nc.c2ps2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_const_NNLO(z, _args):
    return +raw_nc.c2ps2am0_a0(z)


class AsyLLSingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_LL_NNLO, args=[self.L])


class AsyNLLSingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NLL_NNLO, args=[self.L])


class AsyConstSingletVV(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_const_NNLO)


class AsyLLSingletAA(AsyLLSingletVV):
    pass


class AsyNLLSingletAA(AsyNLLSingletVV):
    pass


class AsyConstSingletAA(AsyConstSingletVV):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class PdfMatchingNonSinglet(pc.PdfMatchingNonSinglet):
    pass


# @nb.njit("f8(f8,f8[:])", cache=True)
# def cns_NNLO_reg(z, args):
#     L = args[0]
#     return (
#         raw_nc.c2ns2am0_aq2(z) * L ** 2
#         + raw_nc.c2ns2am0_aq(z) * L
#         + raw_nc.c2ns2am0_a0(z)
#     )


# @nb.njit("f8(f8,f8[:])", cache=True)
# def cns_NNLO_sing(z, args):
#     L = args[0]
#     return (
#         raw_nc.c2ns2bm0_aq2(z) * L ** 2
#         + raw_nc.c2ns2bm0_aq(z) * L
#         + raw_nc.c2ns2bm0_a0(z)
#     )


# @nb.njit("f8(f8,f8[:])", cache=True)
# def cns_NNLO_loc(z, args):
#     L = args[0]
#     return (
#         raw_nc.c2ns2cm0_aq2(z) * L ** 2
#         + raw_nc.c2ns2cm0_aq(z) * L
#         + raw_nc.c2ns2cm0_a0(z)
#     )

# class AsyNonSingletMissing(pc.PartonicChannelAsy):
#     def NNLO(self):
#         return RSL(cns_NNLO_reg, cns_NNLO_sing, cns_NNLO_loc, args=[self.L])


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = intrinsic.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = intrinsic.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = intrinsic.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = intrinsic.Sminus
