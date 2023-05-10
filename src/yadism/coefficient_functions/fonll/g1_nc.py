import numba as nb
import numpy as np

from ..partonic_channel import RSL
from . import g1_nc_raw as raw
from . import partonic_channel as pc


class AsyLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """LL term of massive asymptotic polarized non–singlet Wilson coefficient."""
        return RSL(raw.c2ns_LL_reg, raw.c2ns_LL_loc, args=[self.L])


class AsyNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """NLL term of massive asymptotic polarized non–singlet Wilson coefficient."""
        return RSL(raw.c2ns_NLL_reg, raw.c2ns_NLL_loc, args=[self.L])


class AsyNNLLNonSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """NNLL term of massive asymptotic polarized non–singlet Wilson coefficient."""
        return RSL(raw.c2ns_NNLL_reg, raw.c2ns_NNLL_loc, args=[self.L])


class AsyLLPureSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """LL term of massive asymptotic polarized pure singlet Wilson coefficient."""
        return RSL(raw.c2ps_LL_reg, args=[self.L])


class AsyNLLPureSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """NLL term of massive asymptotic polarized pure singlet Wilson coefficient."""
        return RSL(raw.c2ps_NLL_reg, args=[self.L])


class AsyNNLLPureSinglet(pc.PartonicChannelAsy):
    def NNLO(self):
        """NNLL massive asymptotic polarized pure singlet Wilson coefficient."""
        return RSL(raw.c2ps_NNLL_reg, args=[self.L])


class AsyLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        """LL term of massive asymptotic polarized gluonic Wilson coefficient."""
        return RSL(raw.c2g_LL_reg, args=[self.L])


class AsyNLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        """NLL term of massive asymptotic polarized gluonic Wilson coefficient."""
        return RSL(raw.c2g_NLL_reg, args=[self.L])


class AsyNNLLGluon(pc.PartonicChannelAsy):
    def NNLO(self):
        """NNLL term of massive asymptotic polarized gluonic Wilson coefficient."""
        return RSL(raw.c2g_NNLL_reg, args=[self.L])
