import numpy as np

from yadism.coefficient_functions.asy import g1_nc as f_g1_nc
from yadism.coefficient_functions.asy import g1_nc_raw
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc

from .utils import MockESF


class Test_g1_raw:
    zs = [0.00001, 0.0123, 0.345, 0.678]
    Ls = [0, 1, 10]

    def test_ns(self):
        refs_LL = [
            [-0.8888977777777778, 1.777795555733335, 4 / 3 - 0.000017777866667178354],
            [-0.8998222222222222, 1.7999167538501342, 4 / 3 - 0.02200225967654294],
            [-1.1955555555555555, 2.7141645462256148, 4 / 3 - 0.7522134103944623],
            [-1.4915555555555555, 5.52104899930987, 4 / 3 - 2.014584415000407],
        ]
        refs_NLL = [
            [21.060155130473856, -35.00927026444863, 4 / 9 + 0.00038564659661443766],
            [8.42753185589569, -9.832906887829992, 4 / 9 + 0.16406642957947518],
            [0.88835012027934, 3.2703283716553795, 4 / 9 + 0.44640613270293217],
            [-2.667702147019777, 14.11244914423658, 4 / 9 - 2.119895055120172],
        ]
        refs_NNLL = [
            [-263.5626521950901, 484.40249965037003, 530 / 27 - 0.005980198364992292],
            [-16.386701538397148, 22.11531642483089, 530 / 27 - 0.735761055979515],
            [3.5128057221033555, -8.167217335280759, 530 / 27 + 2.5735901303492197],
            [-15.611471367997643, 39.14863962003579, 530 / 27 - 0.2596281753250294],
        ]
        vals_NNLL = []
        for z in self.zs:
            vals_NNLL.append(
                [
                    g1_nc_raw.c2ns_NNLL_reg(z, np.atleast_1d(np.asarray([0], dtype=float))),
                    g1_nc_raw.c2ns_NNLL_sing(z, np.atleast_1d(np.asarray([0], dtype=float))),
                    g1_nc_raw.c2ns_NNLL_loc(z, np.atleast_1d(np.asarray([0], dtype=float))),
                ]
            )
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(
                    [
                        g1_nc_raw.c2ns_LL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))),
                        g1_nc_raw.c2ns_LL_sing(z, np.atleast_1d(np.asarray([L], dtype=float))),
                        g1_nc_raw.c2ns_LL_loc(z, np.atleast_1d(np.asarray([L], dtype=float))),
                    ]
                )
                vals_NLL.append(
                    [
                        g1_nc_raw.c2ns_NLL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))),
                        g1_nc_raw.c2ns_NLL_sing(z, np.atleast_1d(np.asarray([L], dtype=float))),
                        g1_nc_raw.c2ns_NLL_loc(z, np.atleast_1d(np.asarray([L], dtype=float))),
                    ]
                )
            np.testing.assert_allclose(vals_LL, L**2 * np.array(refs_LL))
            np.testing.assert_allclose(vals_NLL, L * np.array(refs_NLL))

    def test_ps(
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
            vals_NNLL.append(g1_nc_raw.c2ps_NNLL_reg(z, np.atleast_1d(np.asarray([0], dtype=float))))
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(g1_nc_raw.c2ps_LL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))))
                vals_NLL.append(g1_nc_raw.c2ps_NLL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))))
            np.testing.assert_allclose(vals_LL, L**2 * np.array(refs_LL))
            np.testing.assert_allclose(vals_NLL, L * np.array(refs_NLL))

    def test_g(self):
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
            vals_NNLL.append(g1_nc_raw.c2g_NNLL_reg(z, np.atleast_1d(np.asarray([0], dtype=float))))
        np.testing.assert_allclose(vals_NNLL, refs_NNLL)
        for L in self.Ls:
            vals_LL = []
            vals_NLL = []
            for z in self.zs:
                vals_LL.append(g1_nc_raw.c2g_LL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))))
                vals_NLL.append(g1_nc_raw.c2g_NLL_reg(z, np.atleast_1d(np.asarray([L], dtype=float))))
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

    def test_cps(self):
        for nf in [3, 4]:
            cps = h_g1_nc.SingletVV(self.esf, nf, m2hq=self.m2hq)
            cpsasys = [
                f_g1_nc.AsyLLSinglet(self.esf, nf, m2hq=self.m2hq),
                f_g1_nc.AsyNLLSinglet(self.esf, nf, m2hq=self.m2hq),
                f_g1_nc.AsyNNLLSinglet(self.esf, nf, m2hq=self.m2hq),
            ]
            heavy = []
            asy = []
            for z in self.zs:
                order = lambda pc: pc.__getattribute__("NNLO")()
                heavy.append(order(cps).reg(z, order(cps).args["reg"]))
                b = 0.0
                for cpsasy in cpsasys:
                    b += order(cpsasy).reg(z, order(cpsasy).args["reg"])
                asy.append(b)
            np.testing.assert_allclose(heavy, asy, rtol=2.1e-1, err_msg=f"nf={nf}")
