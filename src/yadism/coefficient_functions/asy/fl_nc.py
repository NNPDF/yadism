import adani

from ..light import fl_nc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc
from . import raw_nc


class AsyLLGluon(EmptyPartonicChannel):
    pass


class AsyGluon(pc.NeutralCurrentBaseAsy):
    hs3 = adani.HighScaleSplitLogs(3, "L", "g", "gm")


class AsySinglet(pc.NeutralCurrentBaseAsy):
    hs3 = adani.HighScaleSplitLogs(3, "L", "q", "exact")


class AsyNLLGluon(AsyGluon):
    def NLO(self):
        def cg_NLL_NLO(z, _args):
            return raw_nc.clg1am0_a0(z)

        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        def cg_NLL_NNLO(z, args):
            L = args[0]
            return (raw_nc.clg2am0_aq(z) - raw_nc.clg2am0_af(z)) * L

        return RSL(cg_NLL_NNLO, args=[self.L])

    def N3LO(self):
        def cg_NLL_N3LO(z, args):
            L = -args[0]
            # this term does not depend on nf so setting it to zero
            return self.hs3.NLL(z, 0) * L**2

        return RSL(cg_NLL_N3LO, args=[self.L])


class AsyNNLLGluon(AsyGluon):
    def NNLO(self):
        def cg_NNLL_NNLO(z, _args):
            return raw_nc.clg2am0_a0(z)

        return RSL(cg_NNLL_NNLO)

    def N3LO(self):
        def cg_NNLL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.N2LL(z, nf) * L

        return RSL(cg_NNLL_N3LO, args=[self.L, self.nf])


class AsyNNNLLGluon(AsyGluon):
    def N3LO(self):
        def cg_NNNLL_N3LO(z, args):
            nf = int(args[0])
            return self.hs3.N3LL(z, nf).GetCentral()

        return RSL(cg_NNNLL_N3LO, args=[self.nf])


class AsyLLSinglet(EmptyPartonicChannel):
    pass


class AsyNLLSinglet(AsySinglet):
    def NNLO(self):
        def cps_NLL_NNLO(z, args):
            L = args[0]
            return (raw_nc.clps2am0_aq(z) - raw_nc.clps2am0_af(z)) * L

        return RSL(cps_NLL_NNLO, args=[self.L])

    def N3LO(self):
        def cps_NLL_N3LO(z, args):
            L = -args[0]
            # this term does not depend on nf so setting it to zero
            return self.hs3.NLL(z, 0) * L**2

        return RSL(cps_NLL_N3LO, args=[self.L])


class AsyNNLLSinglet(AsySinglet):
    def NNLO(self):
        def cps_NNLL_NNLO(z, _args):
            return raw_nc.clps2am0_a0(z)

        return RSL(cps_NNLL_NNLO)

    def N3LO(self):
        def cps_NNLL_N3LO(z, args):
            L = -args[0]
            # this term does not depend on nf so setting it to zero
            return self.hs3.N2LL(z, 0) * L

        return RSL(cps_NNLL_N3LO, args=[self.L])


class AsyNNNLLSinglet(AsySinglet):
    def N3LO(self):
        def cps_NNNLL_N3LO(z, args):
            nf = int(args[0])
            return self.hs3.N3LL(z, nf).GetCentral()

        return RSL(cps_NNNLL_N3LO, args=[self.nf])


class AsyLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NLL_NNLO(z, args):
            L = args[0]
            return raw_nc.clns2am0_aq(z) * L

        return RSL(cns_NLL_NNLO, args=[self.L])


class AsyNNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NNLL_NNLO(z, _args):
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
