import adani

from ..light import f2_nc as light
from ..partonic_channel import RSL
from . import partonic_channel as pc
from . import raw_nc


class AsyGluon(pc.NeutralCurrentBaseAsy):
    hs3 = adani.HighScaleSplitLogs(3, "2", "g", "gm")


class AsySinglet(pc.NeutralCurrentBaseAsy):
    hs3 = adani.HighScaleSplitLogs(3, "2", "q", "exact")


class AsyLLGluon(AsyGluon):
    def NLO(self):
        def cg_LL_NLO(z, args):
            L = args[0]
            return raw_nc.c2g1am0_aq(z) * L

        return RSL(cg_LL_NLO, args=[self.L])

    def NNLO(self):
        def cg_LL_NNLO(z, args):
            L = args[0]
            return (raw_nc.c2g2am0_aq2(z) - raw_nc.c2g2am0_aqf(z)) * L**2

        return RSL(cg_LL_NNLO, args=[self.L])

    def N3LO(self):
        def cg_LL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.LL(z, nf) * L**3

        return RSL(cg_LL_N3LO, args=[self.L, self.nf])


class AsyNLLGluon(AsyGluon):
    def NLO(self):
        def cg_NLL_NLO(z, _args):
            return raw_nc.c2g1am0_a0(z)

        return RSL(cg_NLL_NLO, args=[self.L])

    def NNLO(self):
        def cg_NLL_NNLO(z, args):
            L = args[0]
            return (raw_nc.c2g2am0_aq(z) - raw_nc.c2g2am0_af(z)) * L

        return RSL(cg_NLL_NNLO, args=[self.L])

    def N3LO(self):
        def cg_NLL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.NLL(z, nf) * L**2

        return RSL(cg_NLL_N3LO, args=[self.L, self.nf])


class AsyNNLLGluon(AsyGluon):
    def NNLO(self):
        def cg_NNLL_NNLO(z, _args):
            return raw_nc.c2g2am0_a0(z)

        return RSL(cg_NNLL_NNLO)

    def N3LO(self):
        def cg_NNLL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.N2LL(z, nf) * L

        return RSL(cg_NNLL_N3LO, args=[self.L, self.nf])


class AsyNNNLLGluon(AsyGluon):
    variation_map = {-1: 2, 0: 0, 1: 1}

    def N3LO(self):
        def cg_NNNLL_N3LO(z, args):
            nf = int(args[0])
            variation = int(args[1])
            return self.hs3.N3LL(z, nf).ToVect()[self.variation_map[variation]]

        return RSL(cg_NNNLL_N3LO, args=[self.nf, self.n3lo_cf_variation])


class AsyLLSinglet(AsySinglet):
    def NNLO(self):
        def cps_LL_NNLO(z, args):
            L = args[0]
            return (raw_nc.c2ps2am0_aq2(z) - raw_nc.c2ps2am0_aqf(z)) * L**2

        return RSL(cps_LL_NNLO, args=[self.L])

    def N3LO(self):
        def cps_LL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.LL(z, nf) * L**3

        return RSL(cps_LL_N3LO, args=[self.L, self.nf])


class AsyNLLSinglet(AsySinglet):
    def NNLO(self):
        def cps_NLL_NNLO(z, args):
            L = args[0]
            return (raw_nc.c2ps2am0_aq(z) - raw_nc.c2ps2am0_af(z)) * L

        return RSL(cps_NLL_NNLO, args=[self.L])

    def N3LO(self):
        def cps_NLL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.NLL(z, nf) * L**2

        return RSL(cps_NLL_N3LO, args=[self.L, self.nf])


class AsyNNLLSinglet(AsySinglet):
    def NNLO(self):
        def cps_NNLL_NNLO(z, _args):
            return raw_nc.c2ps2am0_a0(z)

        return RSL(cps_NNLL_NNLO)

    def N3LO(self):
        def cps_NNLL_N3LO(z, args):
            L = -args[0]
            nf = int(args[1])
            return self.hs3.N2LL(z, nf) * L

        return RSL(cps_NNLL_N3LO, args=[self.L, self.nf])


class AsyNNNLLSinglet(AsySinglet):
    def N3LO(self):
        def cps_NNNLL_N3LO(z, args):
            nf = int(args[0])
            return self.hs3.N3LL(z, nf).GetCentral()

        return RSL(cps_NNNLL_N3LO, args=[self.nf])


class AsyLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_LL_NNLO_reg(z, args):
            L = args[0]
            return raw_nc.c2ns2am0_aq2(z) * L**2

        def cns_LL_NNLO_sing(z, args):
            L = args[0]
            return raw_nc.c2ns2bm0_aq2(z) * L**2

        def cns_LL_NNLO_loc(z, args):
            L = args[0]
            return raw_nc.c2ns2cm0_aq2(z) * L**2

        return RSL(cns_LL_NNLO_reg, cns_LL_NNLO_sing, cns_LL_NNLO_loc, args=[self.L])


class AsyNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NLL_NNLO_reg(z, args):
            L = args[0]
            return raw_nc.c2ns2am0_aq(z) * L

        def cns_NLL_NNLO_sing(z, args):
            L = args[0]
            return raw_nc.c2ns2bm0_aq(z) * L

        def cns_NLL_NNLO_loc(z, args):
            L = args[0]
            return raw_nc.c2ns2cm0_aq(z) * L

        return RSL(cns_NLL_NNLO_reg, cns_NLL_NNLO_sing, cns_NLL_NNLO_loc, args=[self.L])


class AsyNNLLNonSinglet(pc.NeutralCurrentBaseAsy):
    def NNLO(self):
        def cns_NNLL_NNLO_reg(z, _args):
            return raw_nc.c2ns2am0_a0(z)

        def cns_NNLL_NNLO_sing(z, _args):
            return raw_nc.c2ns2bm0_a0(z)

        def cns_NNLL_NNLO_loc(z, _args):
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
