# -*- coding: utf-8 -*-
import io
import numpy as np
import pytest

import yadism.output


class MockPDFgonly:
    def hasFlavor(self, pid):
        return pid == 21

    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x ** 2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


class TestOutput:
    def test_apply_pdf(self):
        out = dict()
        out["interpolation_xgrid"] = [0.5, 1.0]
        out["xiF"] = 1.0
        out["pids"] = [21, 1]
        out["_ciao"] = "come va?"

        obs = ["F2total", "FLtotal", "F3total"]

        for o in obs:
            o_esf = []
            # test Q2 values
            for Q2 in [1, 10, 100]:
                kin = dict(
                    x=0.5,
                    Q2=Q2,
                    values=[[1, 0], [0, 1]],
                    errors=[[1, 0], [0, 1]],
                )
                # plain
                o_esf.append(kin)

            out[o] = o_esf

        out["F1total"] = None
        stream = io.StringIO(str(out))
        outp = yadism.output.Output.load_yaml(stream)

        ret = outp.apply_pdf(MockPDFgonly())
        for o in obs:
            for a, pra in zip(out[o], ret[o]):
                expexted_res = a["values"][0][0] * a["x"] * a["Q2"]
                expected_err = np.abs(a["values"][0][0]) * a["x"] * a["Q2"]
                assert pytest.approx(pra["result"], 0, 0) == expexted_res
                assert pytest.approx(pra["error"], 0, 0) == expected_err

        # test factorization scale variation
        for xiF in [0.5, 2.0]:
            outp["xiF"] = xiF

            ret = outp.apply_pdf(MockPDFgonly())
            for a, pra in zip(out["F2total"], ret["F2total"]):
                expexted_res = a["values"][0][0] * a["x"] * a["Q2"]
                expected_err = np.abs(a["values"][0][0]) * a["x"] * a["Q2"]
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF ** 2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF ** 2
