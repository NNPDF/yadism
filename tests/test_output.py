# -*- coding: utf-8 -*-
import numpy as np
import pytest

import yadism.output


class MockPDFgonly:
    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x ** 2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


class TestOutput:
    def test_apply_pdf(self):
        out = yadism.output.Output()
        out["xgrid"] = [0.5, 1.0]
        out["xiF"] = 1.0
        out["_ciao"] = "come va?"

        obs = ["F2", "FL", "F3"]

        for o in obs:
            o_esf = []
            # test Q2 values
            for Q2 in [1, 10, 100]:
                kin = dict(
                    x=0.5,
                    Q2=Q2,
                    weights={"g": {21: 2 / 9}, "q": {}},
                    values=dict(q=[0, 1], g=[-1, 0]),
                    errors=dict(q=[1, 0], g=[1, 0]),
                )
                # plain
                o_esf.append(kin)

            out[o] = o_esf

        out["F1"] = None

        ret = out.apply_pdf(MockPDFgonly())
        for o in obs:
            for a, pra in zip(out[o], ret[o]):
                expexted_res = a["values"]["g"][0] * a["x"] * a["Q2"] * 2 / 9
                expected_err = np.abs(a["values"]["g"][0]) * a["x"] * a["Q2"] * 2 / 9
                assert pytest.approx(pra["result"], 0, 0) == expexted_res
                assert pytest.approx(pra["error"], 0, 0) == expected_err

        # test factorization scale variation
        for xiF in [0.5, 2.0]:
            out["xiF"] = xiF

            ret = out.apply_pdf(MockPDFgonly())
            for a, pra in zip(out["F2"], ret["F2"]):
                expexted_res = a["values"]["g"][0] * a["x"] * a["Q2"] * 2 / 9
                expected_err = np.abs(a["values"]["g"][0]) * a["x"] * a["Q2"] * 2 / 9
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF ** 2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF ** 2

    def test_dump(self):
        out = yadism.output.Output()

        out.dump()

    def test_load(self):
        out = yadism.output.Output()

        out.load()
