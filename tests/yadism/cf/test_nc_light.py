import numpy as np

from yadism.coefficient_functions.light import f2_nc, fl_nc

from .test_pc_general import MockESF


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
    """Comparison with exact results provided in
    the source files of https://arxiv.org/abs/2208.14325.
    They follow the convention:

      c_ns = c_{ns} + w2 c_{q,d33}, eq 87
      c_s = c_{ns} + w3 c_{q,d33} + c_{ps}, eq 93
      c_g = c_{g,a} + w3 c_{g,d33}, eq 94


    Reference numbers are obtained with the notebook provided in the arxiv.
    Tables follow the syntax reg, sing, loc
    """

    Q2 = 10
    xgrid = [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.2, 0.3, 0.8]
    nf = 4
    w2 = 1 / 2  # aka fl
    w3 = 1 / 10  # aka fls
    # Cg are already summed with w3 * Cgd33

    def test_f2(self):
        f2_ns_ref = np.array(
            [
                [
                    -25210.90144877971,
                    +1541.5296261447852,
                    -547.2207168022906 - 0.015414917879195673,
                ],
                [
                    -19754.604794494728,
                    +1542.2108232097264,
                    -547.2207168022906 - 0.15418323657594063,
                ],
                [
                    -9363.79003285024,
                    +1549.0339855391976,
                    -547.2207168022906 - 1.5452418733014899,
                ],
                [
                    -4082.1177848093157,
                    +1618.3994999557867,
                    -547.2207168022906 - 15.797135410340475,
                ],
                [
                    -3633.2967291433406,
                    +2442.1103273243853,
                    -547.2207168022906 - 196.61407095029423,
                ],
                [
                    -5010.398131329288,
                    +3726.6274238095793,
                    -547.2207168022906 - 501.12391506634765,
                ],
                [
                    -6859.0499497526125,
                    +5612.869667249117,
                    -547.2207168022906 - 961.8181838278934,
                ],
                [
                    -18895.21889556136,
                    +70966.81668869735,
                    -547.2207168022906 - 12274.642592256147,
                ],
            ]
        )
        f2_ps_ref = [
            8.888925046728956 * 1e8,
            5.373502609122133 * 1e7,
            2.5352195227940553 * 1e6,
            98075.23202808698,
            -1455.5379909662433,
            -3540.9862385762303,
            -3137.28378116819,
            283.9008035816346,
        ]
        f2_q_d33_ref = np.array(
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
            1.902266748856789 * 1e9,
            1.1075727412736598 * 1e8,
            4.633432754458097 * 1e6,
            127252.68332628548,
            -8105.512855135481,
            -12008.601884916112,
            -13224.020410038176,
            30459.55719448865,
        ]
        f2_g_d33_ref = [
            0.3150953791683738,
            -0.5687703649017806,
            -11.108329596244673,
            -51.74326617587184,
            -13.015858269289614,
            78.27078451693676,
            136.31310721643484,
            -107.34906798594845,
        ]

        f2_ns_result = []
        f2_s_result = []
        f2_g_result = []
        for x in self.xgrid:
            esf = MockESF(x, self.Q2)
            f2_ns = f2_nc.NonSinglet(esf, self.nf).N3LO()
            f2_s = f2_nc.Singlet(esf, self.nf).N3LO()
            f2_g = f2_nc.Gluon(esf, self.nf).N3LO()
            f2_q_fl11 = f2_nc.QuarkFL11(esf, self.nf).N3LO()
            f2_g_fl11 = f2_nc.GluonFL11(esf, self.nf).N3LO()
            f2_ns_result.append(
                [
                    f2_ns.reg(x, f2_ns.args["reg"]),
                    f2_ns.sing(x, f2_ns.args["sing"]),
                    f2_ns.loc(x, f2_ns.args["loc"]),
                    f2_q_fl11.reg(x, f2_q_fl11.args["reg"]),
                    f2_q_fl11.loc(x, f2_q_fl11.args["loc"]),
                ]
            )
            f2_s_result.append(f2_s.reg(x, f2_s.args["reg"]))
            f2_g_result.append(
                [
                    f2_g.reg(x, f2_g.args["reg"]),
                    f2_g_fl11.reg(x, f2_g_fl11.args["reg"]),
                ]
            )

        f2_ns_result = np.array(f2_ns_result)
        f2_g_result = np.array(f2_g_result)
        # ns,+ reg
        np.testing.assert_allclose(f2_ns_result[:, 0], f2_ns_ref[:, 0], rtol=3e-4)
        np.testing.assert_allclose(f2_ns_result[:, 3], f2_q_d33_ref[:, 0], rtol=3e-4)
        # ns,+ singular
        np.testing.assert_allclose(f2_ns_result[:, 1], f2_ns_ref[:, 1], rtol=2e-6)
        # ns,+ local
        # Vogt results are shifted, while Bluemlein are exact
        shift = 25.10 + 0.0155 * self.nf**2 - 0.387 * self.nf
        np.testing.assert_allclose(
            f2_ns_result[:, 2] - shift, f2_ns_ref[:, -1], rtol=8e-3
        )
        np.testing.assert_allclose(f2_ns_result[:, -1], f2_q_d33_ref[:, -1], rtol=4e-6)

        # singlet
        np.testing.assert_allclose(f2_s_result, f2_ps_ref, rtol=8e-4)
        # gluon
        np.testing.assert_allclose(f2_g_result[:, 0], f2_g_ref, rtol=8e-4)
        np.testing.assert_allclose(f2_g_result[:, 1], f2_g_d33_ref, rtol=8e-4)

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
                5.488363542270106 * 1e8,
                3.835434031692825 * 1e7,
                2.26712990486453 * 1e6,
                96172.53664094443,
                -1257.6015942775657,
                -2732.319969090693,
                -2665.280165793654,
                -728.12411392513,
            ]
        )
        fl_q_d33_ref = np.array(
            [
                0.19797247888820696,
                0.9628781089693601,
                3.756241841082392,
                10.132317379176609,
                13.720216869793314,
                5.652774770555627,
                -7.019854652912854,
                -82.18354743847462,
            ]
        )
        fl_g_ref = np.array(
            [
                1.210621697704403 * 1e9,
                8.382304167123571 * 1e7,
                4.8328963437255705 * 1e6,
                184641.55589959846,
                -5449.737920292786,
                -10505.515829842048,
                -13510.657754038137,
                10311.159403774058,
            ]
        )
        fl_g_d33_ref = np.array(
            [
                1.032566445095237,
                3.065420125245358,
                3.840329070099055,
                -11.049179587736642,
                -2.198828396045277,
                27.862670577519946,
                39.12606239440606,
                -42.88717253518674,
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
            fl_q_fl11 = fl_nc.QuarkFL11(esf, self.nf).N3LO()
            fl_g_fl11 = fl_nc.GluonFL11(esf, self.nf).N3LO()
            fl_ns_result.append(
                [
                    fl_ns.reg(x, fl_ns.args["reg"]),
                    0,
                    fl_ns.loc(x, fl_ns.args["loc"]),
                    fl_q_fl11.reg(x, fl_q_fl11.args["reg"]),
                ]
            )
            fl_s_result.append(fl_s.reg(x, fl_s.args["reg"]))
            fl_g_result.append(
                [
                    fl_g.reg(x, fl_g.args["reg"]),
                    fl_g_fl11.reg(x, fl_g_fl11.args["reg"]),
                ]
            )

        fl_ns_result = np.array(fl_ns_result)
        fl_g_result = np.array(fl_g_result)

        # Less accurate since Vogt et al. parametrization contains
        # a local part (not physical) that is used to fine tune the accuracy
        # as written in the source fortran files
        # ns,+
        np.testing.assert_allclose(
            fl_ns_result[:, 0],
            fl_ns_ref,
            rtol=3e-3,
        )
        np.testing.assert_allclose(
            fl_ns_result[:, 3],
            fl_q_d33_ref,
            rtol=8e-4,
        )
        # singlet
        np.testing.assert_allclose(
            fl_s_result,
            fl_ps_ref,
            rtol=7e-4,
        )
        # gluon
        np.testing.assert_allclose(fl_g_result[:, 0], fl_g_ref, rtol=9e-4)
        np.testing.assert_allclose(fl_g_result[:, 1], fl_g_d33_ref, rtol=4e-4)
