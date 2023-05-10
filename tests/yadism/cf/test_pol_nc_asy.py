import numpy as np
import pandas as pd
from eko.thresholds import ThresholdsAtlas

from yadism import observable_name as on
from yadism.coefficient_functions.fonll import g1_nc as f_g1_nc
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc


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


def test_cns():
    Q2 = 200
    esf = MockESF("g1_charm", 0.1, Q2)
    m2hq = 2
    df = pd.DataFrame(columns=["nf", "z", "Massive", "FONLL"])
    for nf in [3, 4]:
        for z in [3 * 1e-1, 2 * 1e-1, 1e-1, 1e-2, 1e-3]:
            cg = h_g1_nc.NonSinglet(esf, nf, m2hq=m2hq)
            cgasys = [
                f_g1_nc.AsyLLNonSinglet(esf, nf, m2hq=m2hq),
                f_g1_nc.AsyNLLNonSinglet(esf, nf, m2hq=m2hq),
                f_g1_nc.AsyNNLLNonSinglet(esf, nf, m2hq=m2hq),
            ]
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a = order(cg).reg(z, order(cg).args["reg"])
            b = 0.0
            for cgasy in cgasys:
                if order(cgasy):
                    b += order(cgasy).reg(z, order(cgasy).args["reg"])
            df = df.append(
                {
                    "nf": nf,
                    "z": "{:.3g}".format(z),
                    "Massive": "{:.3g}".format(a),
                    "FONLL": "{:.3g}".format(b),
                },
                ignore_index=True,
            )
            df = df.rename_axis("NS Coefficient Function")
            # np.testing.assert_allclose(
            # a, b, rtol=7e-2, err_msg=f"nf={nf}, z={z},o={o}"
            # )
    print(df)


def test_cg():
    Q2 = 200
    esf = MockESF("g1_charm", 0.1, Q2)
    m2hq = 2
    df = pd.DataFrame(columns=["nf", "z", "Massive", "FONLL"])
    for nf in [3, 4]:
        for z in [3 * 1e-1, 2 * 1e-1, 1e-1, 1e-2, 1e-3]:
            cg = h_g1_nc.NonSinglet(esf, nf, m2hq=m2hq)
            cgasys = [
                f_g1_nc.AsyLLGluon(esf, nf, m2hq=m2hq),
                f_g1_nc.AsyNLLGluon(esf, nf, m2hq=m2hq),
                f_g1_nc.AsyNNLLGluon(esf, nf, m2hq=m2hq),
            ]
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a = order(cg).reg(z, order(cg).args["reg"])
            b = 0.0
            for cgasy in cgasys:
                if order(cgasy):
                    b += order(cgasy).reg(z, order(cgasy).args["reg"])
            df = df.append(
                {
                    "nf": nf,
                    "z": "{:.3g}".format(z),
                    "Massive": "{:.3g}".format(a),
                    "FONLL": "{:.3g}".format(b),
                },
                ignore_index=True,
            )
            # np.testing.assert_allclose(
            # a, b, rtol=7e-2, err_msg=f"nf={nf}, z={z},o={o}"
            # )
            df = df.rename_axis("Gluon Coefficient Function")
    print(df)
