from ..light import fl_nc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc
from . import raw_nc


class AsyLLGluon(EmptyPartonicChannel):
    pass


class AsyNLLGluon(pc.NeutralCurrentBaseAsy):
    def NLO(self):
        def cg_NLL_NLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.clg1am0_a0(z)

        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        def cg_NLL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.clg2am0_aq(z) - raw_nc.clg2am0_af(z)) * L

        return RSL(cg_NLL_NNLO, args=[self.L])


class AsyNNLLGluon(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cg_NNLL_NNLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.clg2am0_a0(z)

        return RSL(cg_NNLL_NNLO)


class AsyNNNLLGluon(pc.NeutralCurrentBaseAsy):
    pass


class AsyLLSinglet(EmptyPartonicChannel):
    pass


class AsyNLLSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cps_NLL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return (raw_nc.clps2am0_aq(z) - raw_nc.clps2am0_af(z)) * L

        return RSL(cps_NLL_NNLO, args=[self.L])


class AsyNNLLSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cps_NNLL_NNLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.clps2am0_a0(z)

        return RSL(cps_NNLL_NNLO)


class AsyNNNLLSinglet(pc.NeutralCurrentBaseAsy):
    pass


class AsyLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NLL_NNLO(z, args):
            if self.is_below_pair_threshold(z):
                return 0.0
            L = args[0]
            return raw_nc.clns2am0_aq(z) * L

        return RSL(cns_NLL_NNLO, args=[self.L])


class AsyNNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NNLL_NNLO(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return raw_nc.clns2am0_a0(z)

        return RSL(cns_NNLL_NNLO)


class AsyNNNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyLLIntrinsic(pc.PartonicChannelAsyLLIntrinsic):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicMatching(pc.PartonicChannelAsyNLLIntrinsicMatching):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicLight(pc.PartonicChannelAsyNLLIntrinsicLight):
    light_cls = light.NonSinglet
