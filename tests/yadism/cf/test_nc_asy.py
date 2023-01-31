import numpy as np
from eko.thresholds import ThresholdsAtlas

from yadism import observable_name as on
from yadism.coefficient_functions.fonll import f2_nc as f_f2_nc
from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc


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


class MockInfo:
    threshold = None


class MockESF:
    def __init__(self, sf, x, Q2):
        self.sf = MockSF(sf)
        self.x = x
        self.Q2 = Q2
        self.process = "NC"
        self.info = MockInfo()
        self.info.threshold = self.sf.threshold


def test_cg():
    Q2 = 200
    esf = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg = h_f2_nc.GluonVV(esf, nf, m2hq=m2hq)
            cgasys = [
                f_f2_nc.AsyLLGluon(esf, nf, mu2hq=m2hq),
                f_f2_nc.AsyNLLGluon(esf, nf, mu2hq=m2hq),
                f_f2_nc.AsyNNLLGluon(esf, nf, mu2hq=m2hq),
            ]
            for o in ["NLO", "NNLO"]:
                order = lambda pc, o=o: pc.__getattribute__(o)()
                a = order(cg).reg(z, order(cg).args["reg"])
                b = 0.0
                for cgasy in cgasys:
                    if order(cgasy):
                        b += order(cgasy).reg(z, order(cgasy).args["reg"])
                np.testing.assert_allclose(
                    a, b, rtol=7e-2, err_msg=f"nf={nf}, z={z},o={o}"
                )
