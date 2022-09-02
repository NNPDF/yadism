# -*- coding: utf-8 -*-
import numpy as np
from test_pc_general import MockESF

from yadism.coefficient_functions.light import f3_cc


def test_N3LO_labels():
    Q2 = 200
    x = 0.1
    esf = MockESF(x, Q2)
    nf = 3
    f3_ns = f3_cc.NonSingletOdd(esf, nf)

    assert f3_ns.N3LO().args["reg"] is not None
    assert f3_ns.N3LO().args["loc"] is not None
    assert f3_ns.N3LO().args["sing"] is not None


class Test_Blumlein_results:
    """Comparison with exact results provided in https://arxiv.org/pdf/2208.14325.pdf.
    They follow the convention:

      c_ns  = c_{ns} + c_{q,d33}

    Reference numbers are obtained with the notebook provided in the arxiv.
    Tables  follow the syntax reg, sing, loc
    """

    Q2 = 10
    xgrid = [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.2, 0.3, 0.8]
    nf = 4

    def test_f3_bluemlein(self):
        f3_ns_ref = np.array(
            [
                [
                    -25231.429850963934,
                    1541.529626144562,
                    -547.2207168022869 - 0.015414917879195668,
                ],
                [
                    -10211.246584770022,
                    1542.2108232096089,
                    -547.2207168023251 - 0.1541832365759406,
                ],
                [
                    -2080.6483437193,
                    1549.033985539169,
                    -547.2207168023015 - 1.5452418733014894,
                ],
                [
                    -1582.042993312226,
                    1618.3994999557885,
                    -547.2207168022896 - 15.797135410340472,
                ],
                [
                    -3137.5438037392723,
                    2442.110327324382,
                    -547.2207168023087 - 196.61407095029418,
                ],
                [
                    -4369.890283850198,
                    3726.627423809562,
                    -547.2207168023033 - 501.12391506634765,
                ],
                [
                    -6023.31882637291,
                    5612.869667249121,
                    -547.2207168022851 - 961.8181838278933,
                ],
                [
                    -18980.411027186972,
                    70966.81668869738,
                    -547.2207168022705 - 12274.64259225615,
                ],
            ]
        )
        f3_d33_ref = np.zeros_like(f3_ns_ref)
        f3_d33_ref[:, 0] = [
            335157.49517575925,
            81453.24831397024,
            5166.17350678876,
            -3761.984881346483,
            4.725655474352505,
            401.9708197245185,
            407.6694782016153,
            85.2476397632709,
        ]

        f3_ns_result = []
        for x in self.xgrid:
            esf = MockESF(x, self.Q2)
            f3_ns = f3_cc.NonSingletOdd(esf, self.nf).N3LO()
            f3_ns_result.append(
                [
                    f3_ns.reg(x, f3_ns.args["reg"]),
                    f3_ns.sing(x, f3_ns.args["sing"]),
                    f3_ns.loc(x, f3_ns.args["loc"]),
                ]
            )

        # ns,+
        np.testing.assert_allclose(
            np.array(f3_ns_result)[:, :-1], (f3_ns_ref + f3_d33_ref)[:, :-1], rtol=3e-4
        )
        np.testing.assert_allclose(
            np.array(f3_ns_result)[:, -1], (f3_ns_ref + f3_d33_ref)[:, -1], rtol=5e-2
        )
