# -*- coding: utf-8 -*-

import numba as nb
from eko.constants import TR

from ..intrinsic import f2_nc as intrinsic
from ..light import f2_nc as light
from ..partonic_channel import RSL
from ..splitting_functions import lo
from . import partonic_channel as pc
from . import raw_nc


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NLO(z, args):
    L = args[0]
    return raw_nc.c2g1am0_aq(z) * L + raw_nc.c2g1am0_a0(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def cg_NNLO(z, args):
    L = args[0]
    return (
        raw_nc.c2g2am0_aq2(z) * L ** 2 + raw_nc.c2g2am0_aq(z) * L + raw_nc.c2g2am0_a0(z)
    )


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


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLO_reg(z, args):
    L = args[0]
    return (
        raw_nc.c2ns2am0_aq2(z) * L ** 2
        + raw_nc.c2ns2am0_aq(z) * L
        + raw_nc.c2ns2am0_a0(z)
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLO_sing(z, args):
    L = args[0]
    return (
        raw_nc.c2ns2bm0_aq2(z) * L ** 2
        + raw_nc.c2ns2bm0_aq(z) * L
        + raw_nc.c2ns2bm0_a0(z)
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def cns_NNLO_loc(z, args):
    L = args[0]
    return (
        raw_nc.c2ns2cm0_aq2(z) * L ** 2
        + raw_nc.c2ns2cm0_aq(z) * L
        + raw_nc.c2ns2cm0_a0(z)
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_reg(z, args):
    L = args[0]
    as_norm = 2.0
    return L ** 2 / 2.0 * 2.0 * TR / 3 * as_norm * lo.pqq_reg(z, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_sing(z, args):
    L = args[0]
    as_norm = 2.0
    return (
        pc.K_qq_sing(z)
        + L ** 2 / 2.0 * 2.0 * TR / 3 * as_norm * lo.pqq_sing(z, args)
        - L * pc.Delta_qq_sing(z)
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_loc(z, args):
    L = args[0]
    as_norm = 2.0
    return (
        pc.K_qq_loc(z)
        + L ** 2 / 2.0 * 2.0 * TR / 3 * as_norm * lo.pqq_local(z, args)
        - L * pc.Delta_qq_loc(z)
    )


class PdfMatchingNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(pdf_matching_reg, pdf_matching_sing, pdf_matching_loc, args=[self.L])


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class AsyNonSingletMissing(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(cns_NNLO_reg, cns_NNLO_sing, cns_NNLO_loc, args=[self.L])


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = intrinsic.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = intrinsic.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = intrinsic.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = intrinsic.Sminus
