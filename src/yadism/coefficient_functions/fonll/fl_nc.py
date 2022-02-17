# -*- coding: utf-8 -*-

import numba as nb

from ..intrinsic import fl_nc as intrinsic
from ..light import fl_nc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLL_NLO(z, _args):
    return raw_nc.clg1am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLL_NNLO(z, args):
    L = args[0]
    return (raw_nc.clg2am0_aq(z) - raw_nc.clg2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NNLL_NNLO(z, _args):
    return raw_nc.clg2am0_a0(z)


class AsyLLGluon(EmptyPartonicChannel):
    pass


class AsyNLLGluon(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        return RSL(cg_NLL_NNLO, args=[self.L])


class AsyNNLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cg_NNLL_NNLO)


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NLL_NNLO(z, args):
    L = args[0]
    return (raw_nc.clps2am0_aq(z) - raw_nc.clps2am0_af(z)) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def cps_NNLL_NNLO(z, _args):
    return raw_nc.clps2am0_a0(z)


class AsyLLSinglet(EmptyPartonicChannel):
    pass


class AsyNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NLL_NNLO, args=[self.L])


class AsyNNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cps_NNLL_NNLO)


class AsyLLNonSinglet(EmptyPartonicChannel):
    pass


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NLL_NNLO(z, args):
    L = args[0]
    return raw_nc.clns2am0_aq(z) * L


class AsyNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NLL_NNLO)


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLL_NNLO(z, _args):
    return raw_nc.clns2am0_a0(z)


class AsyNNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NNLL_NNLO)


class PdfMatchingLLNonSinglet(EmptyPartonicChannel):
    pass


class PdfMatchingNLLNonSinglet(EmptyPartonicChannel):
    pass


class PdfMatchingNNLLNonSinglet(EmptyPartonicChannel):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = intrinsic.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = intrinsic.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = intrinsic.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = intrinsic.Sminus
