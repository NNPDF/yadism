from ..light import f2_nc as light
from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_nc


class AsyLLGluon(pc.NeutralCurrentBaseAsy):
    def NLO(self):
        def cg_LL_NLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2g1am0_aq(z) * L

        return RSL(cg_LL_NLO, args=[self.L])

    def NNLO(self):
        def cg_LL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.c2g2am0_aq2(z) - raw_nc.c2g2am0_aqf(z)) * L**2

        return RSL(cg_LL_NNLO, args=[self.L])


class AsyNLLGluon(pc.NeutralCurrentBaseAsy):
    def NLO(self):
        def cg_NLL_NLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2g1am0_a0(z)

        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        def cg_NLL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.c2g2am0_aq(z) - raw_nc.c2g2am0_af(z)) * L

        return RSL(cg_NLL_NNLO, args=[self.L])


class AsyNNLLGluon(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cg_NNLL_NNLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2g2am0_a0(z)

        return RSL(cg_NNLL_NNLO)


class AsyNNNLLGluon(pc.NeutralCurrentBaseAsy):
    pass


class AsyLLSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cps_LL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.c2ps2am0_aq2(z) - raw_nc.c2ps2am0_aqf(z)) * L**2

        return RSL(cps_LL_NNLO, args=[self.L])


class AsyNLLSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cps_NLL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.c2ps2am0_aq(z) - raw_nc.c2ps2am0_af(z)) * L

        return RSL(cps_NLL_NNLO, args=[self.L])


class AsyNNLLSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cps_NNLL_NNLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2ps2am0_a0(z)

        return RSL(cps_NNLL_NNLO)


class AsyNNNLLSinglet(pc.NeutralCurrentBaseAsy):
    pass


class AsyLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_LL_NNLO_reg(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2am0_aq2(z) * L**2

        def cns_LL_NNLO_sing(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2bm0_aq2(z) * L**2

        def cns_LL_NNLO_loc(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2cm0_aq2(z) * L**2

        return RSL(cns_LL_NNLO_reg, cns_LL_NNLO_sing, cns_LL_NNLO_loc, args=[self.L])


class AsyNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NLL_NNLO_reg(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2am0_aq(z) * L

        def cns_NLL_NNLO_sing(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2bm0_aq(z) * L

        def cns_NLL_NNLO_loc(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.c2ns2cm0_aq(z) * L

        return RSL(cns_NLL_NNLO_reg, cns_NLL_NNLO_sing, cns_NLL_NNLO_loc, args=[self.L])


class AsyNNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NNLL_NNLO_reg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2ns2am0_a0(z)

        def cns_NNLL_NNLO_sing(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2ns2bm0_a0(z)

        def cns_NNLL_NNLO_loc(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.c2ns2cm0_a0(z)

        return RSL(cns_NNLL_NNLO_reg, cns_NNLL_NNLO_sing, cns_NNLL_NNLO_loc)


class AsyNNNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    pass


class AsyLLIntrinsic(pc.PartonicChannelAsyLLIntrinsic):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicMatching(pc.PartonicChannelAsyNLLIntrinsicMatching):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicLight(pc.PartonicChannelAsyNLLIntrinsicLight):
    light_cls = light.NonSinglet
