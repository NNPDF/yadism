from ..partonic_channel import RSL
from . import g1_nc_raw as raw
from . import partonic_channel as pc


class AsyLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2ns_LL_reg, raw.c2ns_LL_sing, raw.c2ns_LL_loc, args=[self.L])


class AsyNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2ns_NLL_reg, raw.c2ns_NLL_sing, raw.c2ns_NLL_loc, args=[self.L])


class AsyNNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(
            raw.c2ns_NNLL_reg, raw.c2ns_NNLL_sing, raw.c2ns_NNLL_loc, args=[self.L]
        )


class AsyLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2ps_LL_reg, args=[self.L])


class AsyNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2ps_NLL_reg, args=[self.L])


class AsyNNLLSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2ps_NNLL_reg, args=[self.L])


class AsyLLGluon(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(raw.c1g_LL_reg, args=[self.L])

    def NNLO(self):
        return RSL(raw.c2g_LL_reg, args=[self.L])


class AsyNLLGluon(pc.PartonicChannelAsy):
    def NLO(self):
        return RSL(raw.c1g_NLL_reg, args=[self.L])

    def NNLO(self):
        return RSL(raw.c2g_NLL_reg, args=[self.L])


class AsyNNLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        return RSL(raw.c2g_NNLL_reg, args=[self.L])


class PdfMatchingLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        pass
        # TODO: inset here the LL (L**2) terms for the matching
        # NOTE: if equals to the unpolarized case, just import from there.
        # you can use the syntax:
        # return RSL(sing=A_qq_sing, loc=A_qq_loc, args=[self.L])


class PdfMatchingNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        pass
        # TODO: inset here the NLL (L) terms for the matching


class PdfMatchingNNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        pass
        # TODO: inset here the NNLL (L) terms for the matching


class PdfMatchingNNNLLNonSinglet(pc.PartonicChannelAsy):
    pass
