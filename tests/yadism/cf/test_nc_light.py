# -*- coding: utf-8 -*-

import numpy as np
from eko.constants import CA, CF, TR
from eko.harmonics.constants import zeta2 as z2
from eko.harmonics.constants import zeta3 as z3
from test_pc_general import MockESF

from yadism.coefficient_functions.light import f2_nc, fl_nc


def test_N3LO_labels():
    Q2 = 200
    x = 0.1
    esf = MockESF(x, Q2)
    nf = 3
    fl_ns = fl_nc.NonSinglet(esf, nf)
    f2_ns = f2_nc.NonSinglet(esf, nf)

    assert fl_ns.N3LO().args["reg"] is not None
    assert fl_ns.N3LO().args["loc"] is not None
    assert f2_ns.N3LO().args["reg"] is not None
    assert f2_ns.N3LO().args["loc"] is not None
    assert f2_ns.N3LO().args["sing"] is not None

    fl_g = fl_nc.Gluon(esf, nf)
    f2_g = f2_nc.Gluon(esf, nf)

    assert fl_g.N3LO().args["reg"] is not None
    assert f2_g.N3LO().args["reg"] is not None
    assert f2_g.N3LO().args["loc"] is not None

    fl_s = fl_nc.Singlet(esf, nf)
    f2_s = f2_nc.Singlet(esf, nf)

    assert fl_s.N3LO().args["reg"] is not None
    assert f2_s.N3LO().args["reg"] is not None
    assert f2_s.N3LO().args["loc"] is not None


class Test_Blumlein_results:
    """Comparison with exact results provided in https://arxiv.org/pdf/2208.14325.pdf.
    They follow the convention:

      c_ns  = c_{ns} + w2 c_{q,d33},  eq 87
      c_s  = c_{ns} + w3 c_{q,d33} + c_{ps}, eq 93
      c_g = c_{g,a} + w3 c_{g,d33},  eq 94


    Reference numbers are obtained with the notebook provided in the arxiv.
    Tables  follow the syntax reg, sing, loc
    """

    Q2 = 10
    xgrid = [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.2, 0.3, 0.8]
    nf = 4
    w2 = 1 / 2
    w3 = 1 / 10

    def test_f2(self):
        f2_ns_ref = np.array(
            [
                [-25210.90144877971, +1541.5296261447852, -547.2207168022906],
                [-19754.604794494728, +1542.2108232097264, -547.2207168022906],
                [-9363.79003285024, +1549.0339855391976, -547.2207168022906],
                [-4082.1177848093157, +1618.3994999557867, -547.2207168022906],
                [-3633.2967291433406, +2442.1103273243853, -547.2207168022906],
                [-5010.398131329288, +3726.6274238095793, -547.2207168022906],
                [-6859.0499497526125, +5612.869667249117, -547.2207168022906],
                [-18895.21889556136, +70966.81668869735, -547.2207168022906],
            ]
        )
        f2_ps_ref = np.zeros_like(f2_ns_ref)
        f2_ps_ref[:, 0] = [
            8.888925046728956 * 1e8,
            5.373502609122133 * 1e7,
            2.5352195227940553 * 1e6,
            98075.23202808698,
            -1455.5379909662433,
            -3540.9862385762303,
            -3137.28378116819,
            283.9008035816346,
        ]
        f2_d33_ref = np.array(
            [
                [0.11297488044669358, 0, -47.55183089138901],
                [0.3846176156886669, 0, -47.55183089138901],
                [0.18857989799645086, 0, -47.55183089138901],
                [-8.439985716915114, 0, -47.55183089138901],
                [-52.669673008877886, 0, -47.55183089138901],
                [-74.70535071447053, 0, -47.55183089138901],
                [-87.27834665482078, 0, -47.55183089138901],
                [-100.94803044091451, 0, -47.55183089138901],
            ]
        )
        f2_g_ref = [
            1.9022667488882987 * 1e9,
            1.1075727407048894 * 1e8,
            4.633431643625137 * 1e6,
            127247.50899966789,
            -8106.81444096241,
            -12000.774806464418,
            -13210.389099316533,
            30448.822287690055,
        ]

        f2_ns_result = []
        f2_s_result = []
        f2_g_result = []
        for x in self.xgrid:
            esf = MockESF(x, self.Q2)
            f2_ns = f2_nc.NonSinglet(esf, self.nf).N3LO()
            f2_s = f2_nc.Singlet(esf, self.nf).N3LO()
            f2_g = f2_nc.Gluon(esf, self.nf).N3LO()
            f2_ns_result.append(
                [
                    f2_ns.reg(x, f2_ns.args["reg"]),
                    f2_ns.sing(x, f2_ns.args["sing"]),
                    f2_ns.loc(x, f2_ns.args["loc"]),
                ]
            )
            f2_s_result.append(
                [
                    f2_s.reg(x, f2_s.args["reg"]),
                    0,
                    f2_s.loc(x, f2_s.args["loc"]),
                ]
            )
            f2_g_result.append(f2_g.reg(x, f2_g.args["reg"]))

        f2_ns_result = np.array(f2_ns_result)
        f2_s_result = np.array(f2_s_result)
        # Local pieces do not match ...
        # ns,+
        np.testing.assert_allclose(
            f2_ns_result[:, :-1],
            (f2_ns_ref + self.w2 * f2_d33_ref)[:, :-1],
            rtol=5e-3,
        )
        # singlet
        np.testing.assert_allclose(
            (f2_s_result + f2_ns_result)[:, :-1],
            (f2_ps_ref + self.w3 * f2_d33_ref + f2_ns_ref)[:, :-1],
            rtol=2e-3,
        )
        # gluon
        np.testing.assert_allclose(f2_g_result, f2_g_ref, rtol=8e-4)

    def test_fl(self):
        fl_ns_ref = np.array(
            [
                5231.672605793465,
                1113.5910200378567,
                -416.798839922202,
                -525.9575405270043,
                -332.26359517009996,
                -479.21194890176344,
                -691.2885632994945,
                -254.87983159274881,
            ]
        )
        fl_ps_ref = np.array(
            [
                5.48836 * 1e8,
                3.83543 * 1e7,
                2.26713 * 1e6,
                96172.5,
                -1257.6,
                -2732.32,
                -2665.28,
                -728.124,
            ]
        )
        fl_d33_ref = np.array(
            [
                0.197972,
                0.962878,
                3.75624,
                10.1323,
                13.7202,
                5.65277,
                -7.01985,
                -82.1835,
            ]
        )
        fl_g_ref = np.array(
            [
                1.21062 * 1e9,
                8.3823 * 1e7,
                4.8329 * 1e6,
                184640.0,
                -5449.96,
                -10502.7,
                -13506.7,
                10306.9,
            ]
        )

        fl_ns_result = []
        fl_s_result = []
        fl_g_result = []
        for x in self.xgrid:
            esf = MockESF(x, self.Q2)
            fl_ns = fl_nc.NonSinglet(esf, self.nf).N3LO()
            fl_s = fl_nc.Singlet(esf, self.nf).N3LO()
            fl_g = fl_nc.Gluon(esf, self.nf).N3LO()
            fl_ns_result.append(
                [
                    fl_ns.reg(x, fl_ns.args["reg"]),
                    0,
                    fl_ns.loc(x, fl_ns.args["loc"]),
                ]
            )
            fl_s_result.append(fl_s.reg(x, fl_s.args["reg"]))
            fl_g_result.append(fl_g.reg(x, fl_g.args["reg"]))

        fl_ns_result = np.array(fl_ns_result)
        fl_s_result = np.array(fl_s_result)

        # Less accurate since Vogt et al. parametrization contains
        # a local part (not physical) that is used to compensate the accuracy
        # ns,+
        np.testing.assert_allclose(
            fl_ns_result[:, 0],
            fl_ns_ref + self.w2 * fl_d33_ref,
            rtol=9e-2,
        )
        # singlet
        np.testing.assert_allclose(
            fl_s_result + fl_ns_result[:, 0],
            fl_ps_ref + self.w3 * fl_d33_ref + fl_ns_ref,
            rtol=1e-2,
        )
        # gluon
        np.testing.assert_allclose(fl_g_result, fl_g_ref, rtol=8e-4)
