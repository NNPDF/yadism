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
def cg_NLL_NLO(z, _args):
    return raw_nc.c2g1am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_LL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2g2am0_aq2(z) - raw_nc.c2g2am0_aqf(z)) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2g2am0_aq(z) - raw_nc.c2g2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NNLL_NNLO(z, _args):
    return raw_nc.c2g2am0_a0(z)


class AsyLLGluon(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_LL_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_LL_NNLO, args=[self.L])


class AsyNLLGluon(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_NLL_NNLO, args=[self.L])


class AsyNNLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cg_NNLL_NNLO)


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_LL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2ps2am0_aq2(z) - raw_nc.c2ps2am0_aqf(z)) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NLL_NNLO(z, args):
    L = args[0]
    return (raw_nc.c2ps2am0_aq(z) - raw_nc.c2ps2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NNLL_NNLO(z, _args):
    return raw_nc.c2ps2am0_a0(z)


class AsyLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_LL_NNLO, args=[self.L])


class AsyNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NLL_NNLO, args=[self.L])


class AsyNNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NNLL_NNLO)


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_LL_NNLO_reg(z, args):
    L = args[0]
    return raw_nc.c2ns2am0_aq2(z) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_LL_NNLO_sing(z, args):
    L = args[0]
    return raw_nc.c2ns2bm0_aq2(z) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_LL_NNLO_loc(z, args):
    L = args[0]
    return raw_nc.c2ns2cm0_aq2(z) * L**2


class AsyLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_LL_NNLO_reg, cns_LL_NNLO_sing, cns_LL_NNLO_loc, args=[self.L])


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NLL_NNLO_reg(z, args):
    L = args[0]
    return raw_nc.c2ns2am0_aq(z) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NLL_NNLO_sing(z, args):
    L = args[0]
    return raw_nc.c2ns2bm0_aq(z) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NLL_NNLO_loc(z, args):
    L = args[0]
    return raw_nc.c2ns2cm0_aq(z) * L


class AsyNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NLL_NNLO_reg, cns_NLL_NNLO_sing, cns_NLL_NNLO_loc, args=[self.L])


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLL_NNLO_reg(z, _args):
    return raw_nc.c2ns2am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLL_NNLO_sing(z, _args):
    return raw_nc.c2ns2bm0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLL_NNLO_loc(z, _args):
    return raw_nc.c2ns2cm0_a0(z)


class AsyNNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NNLL_NNLO_reg, cns_NNLL_NNLO_sing, cns_NNLL_NNLO_loc)


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class PdfMatchingLLNonSinglet(pc.PdfMatchingLLNonSinglet):
    pass


class PdfMatchingNLLNonSinglet(pc.PdfMatchingNLLNonSinglet):
    pass


class PdfMatchingNNLLNonSinglet(pc.PdfMatchingNNLLNonSinglet):
    pass


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = intrinsic.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = intrinsic.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = intrinsic.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = intrinsic.Sminus
