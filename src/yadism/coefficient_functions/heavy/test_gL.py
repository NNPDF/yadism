import matplotlib.pyplot as plt
import numpy as np
from eko.thresholds import ThresholdsAtlas

from yadism import observable_name as on
from yadism.coefficient_functions.heavy import fl_nc as h_fl_nc
from yadism.coefficient_functions.heavy import gl_nc as h_gl_nc


class MockCouplingConstants:
    def get_weight(self, _pid, _q2, qct):
        if qct == "VV":
            return 1
        if qct == "VA":
            return 2
        if qct == "AV":
            return 4
        if qct == "AA":
            return 8
        raise ValueError(f"Unkown {qct}")


class MockSF:
    def __init__(self, n):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants()
        self.m2hq = [1.0, 2.0, 3.0]
        self.threshold = ThresholdsAtlas(self.m2hq)


class MockESF:
    def __init__(self, sf, x, Q2):
        self.sf = MockSF(sf)
        self.x = x
        self.Q2 = Q2
        self.process = "NC"


def test_cg_NNLO():
    Q2 = 200
    esf1 = MockESF("gL_charm", 0.1, Q2)
    esf2 = MockESF("FL_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_gl_nc.NonSinglet(esf1, nf, m2hq=m2hq)
            cg_2 = h_fl_nc.NonSinglet(esf2, nf, m2hq=m2hq)
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a_1 = order(cg_1).reg(
                z, order(cg_1).args["reg"]
            )  # sing and loc the same (?)
            a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                -a_2,
                err_msg="gL and FL coefficients at NNLO should be the same, but are not",
            )
