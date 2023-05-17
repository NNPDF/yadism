import numpy as np

from yadism.coefficient_functions.fonll import g1_nc as f_g1_nc
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc
from yadism.coefficient_functions.fonll import g1_nc_raw


from test_nc_asy import MockESF


class Test_g1_raw:
    zs = [0.00001, 0.0123, 0.345, 0.678]
    Ls = [0, 1, 10]

    def test_NS(
        self,
    ):
        refs_LL = [
            [0.888897777955557, 4 / 3],
            [0.9000945316279121, 4 / 3],
            [1.5186089906700588, 4 / 3],
            [4.029493443754314, 4 / 3],
        ]
        refs_NLL = [
            [-13.94911513397478, 4 / 9],
            [-1.405375031934304, 4 / 9],
            [4.158678491934721, 4 / 9],
            [11.444746997216804, 4 / 9],
        ]
        refs_NNLL = [
            [220.83984745527997, 530 / 27],
            [5.728614886433739, 530 / 27],
            [-4.654411613177409, 530 / 27],
            [23.537168252038146, 530 / 27],
        ]
        vals_NNLL = []
        for z in self.zs:
            vals_NNLL.append(
                [g1_nc_raw.c2ns_NNLL_reg(z, [0]), g1_nc_raw.c2ns_NNLL_loc(z, [0])]
            )
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(
                    [g1_nc_raw.c2ns_LL_reg(z, [L]), g1_nc_raw.c2ns_LL_loc(z, [L])]
                )
                vals_NLL.append(
                    [g1_nc_raw.c2ns_NLL_reg(z, [L]), g1_nc_raw.c2ns_NLL_loc(z, [L])]
                )
            np.testing.assert_allclose(vals_LL, L**2 * np.array(refs_LL))
            np.testing.assert_allclose(vals_NLL, L * np.array(refs_NLL))

    def test_PS(
        self,
    ):
        refs_LL = [
            48.06968316919936,
            10.576017789909288,
            -1.0993940836064255,
            -0.8155508855037752,
        ]
        refs_NLL = [
            -640.1931101828336,
            -76.57675059123939,
            -4.829440429929221,
            -1.777204251596132,
        ]
        refs_NNLL = [
            -1255.2437541612783,
            148.82388396760942,
            8.499990421142337,
            9.185464893221521,
        ]
        vals_NNLL = []
        for z in self.zs:
            vals_NNLL.append(g1_nc_raw.c2ps_NNLL_reg(z, [0]))
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(g1_nc_raw.c2ps_LL_reg(z, [L]))
                vals_NLL.append(g1_nc_raw.c2ps_NLL_reg(z, [L]))
            np.testing.assert_allclose(vals_LL, L**2 * np.array(refs_LL))
            np.testing.assert_allclose(vals_NLL, L * np.array(refs_NLL))

    def test_g(
        self,
    ):
        refs_LL = [
            178.94641371183462,
            29.519837613005762,
            -10.148135778358451,
            -0.950256937912481,
        ]
        refs_NLL = [
            -1970.4003195041385,
            -168.56223866849194,
            16.559901373764724,
            2.863933384688224,
        ]
        refs_NNLL = [
            -4344.077339368944,
            476.4713474675223,
            -51.14898264499218,
            83.66969562398963,
        ]
        vals_NNLL = []
        for z in self.zs:
            vals_NNLL.append(g1_nc_raw.c2g_NNLL_reg(z, [0]))
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(g1_nc_raw.c2g_LL_reg(z, [L]))
                vals_NLL.append(g1_nc_raw.c2g_NLL_reg(z, [L]))
            np.testing.assert_allclose(vals_LL, L**2 * np.array(refs_LL))
            np.testing.assert_allclose(vals_NLL, L * np.array(refs_NLL))


class Test_limits:
    Q2 = 200
    m2hq = 2
    zs = [3 * 1e-1, 2 * 1e-1, 1e-1, 1e-2, 1e-3]
    esf = MockESF("g1_charm", 0.1, Q2)

    def test_cg(self):
        for nf in [3, 4]:
            cg = h_g1_nc.GluonVV(self.esf, nf, m2hq=self.m2hq)
            cgasys = [
                f_g1_nc.AsyLLGluon(self.esf, nf, m2hq=self.m2hq),
                f_g1_nc.AsyNLLGluon(self.esf, nf, m2hq=self.m2hq),
                f_g1_nc.AsyNNLLGluon(self.esf, nf, m2hq=self.m2hq),
            ]
            for o in ["NLO", "NNLO"]:
                heavy = []
                asy = []
                for z in self.zs:
                    order = lambda pc, o=o: pc.__getattribute__(o)()
                    heavy.append(order(cg).reg(z, order(cg).args["reg"]))
                    b = 0.0
                    for cgasy in cgasys:
                        if order(cgasy):
                            b += order(cgasy).reg(z, order(cgasy).args["reg"])
                    asy.append(b)
                np.testing.assert_allclose(
                    heavy, asy, rtol=2.5e-1, err_msg=f"nf={nf}, o={o}"
                )
