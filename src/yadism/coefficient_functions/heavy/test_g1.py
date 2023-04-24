import matplotlib.pyplot as plt
import numpy as np
from eko.thresholds import ThresholdsAtlas

from yadism import observable_name as on
from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc
from yadism.coefficient_functions.heavy import f3_nc as h_f3_nc
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc


class MockCouplingConstants:
    def get_weight(self, _pid, _q2, qct):
        if qct == "VV":
            return 1
        if qct == "VA":  # -->  must be 0 due to symmetry reasons
            return 2
        if qct == "AV":  # -->  must be 0 due to symmetry reasons
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


def test_cg():
    Q2 = 200
    esf = MockESF("g1_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_g1_nc.GluonVV(esf, nf, m2hq=m2hq)
            cg_2 = h_g1_nc.GluonAA(esf, nf, m2hq=m2hq)
            for o in ["NLO", "NNLO"]:
                order = lambda pc, o=o: pc.__getattribute__(o)()
                a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
                a_2 = order(cg_2).reg(z, order(cg_1).args["reg"])


def test_cg_NLO():
    Q2 = 200
    esf = MockESF("g1_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_g1_nc.GluonVV(esf, nf, m2hq=m2hq)
            cg_2 = h_g1_nc.GluonAA(esf, nf, m2hq=m2hq)
            order = lambda pc, o="NLO": pc.__getattribute__("NLO")()
            a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
            a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                a_2,
                err_msg="AA and VV coefficients at NLO should be the same, but are not",
            )


def test_cg_NNLO():
    Q2 = 200
    esf1 = MockESF("g1_charm", 0.1, Q2)
    esf2 = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_g1_nc.GluonVV(esf1, nf, m2hq=m2hq)
            cg_2 = h_f2_nc.GluonVV(esf2, nf, m2hq=m2hq)
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
            a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                a_2,
                err_msg="g1 and F2 coefficients at NNLO should be the same, but are not",
            )


def test_dq():
    Q2 = 200
    esf1 = MockESF("g1_charm", 0.1, Q2)
    esf2 = MockESF("F3_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            dq_1 = h_g1_nc.NonSinglet(esf1, nf, m2hq=m2hq)
            dq_2 = h_f3_nc.NonSinglet(esf2, nf, m2hq=m2hq)
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a_1 = order(dq_1).reg(z, order(dq_1).args["reg"])
            a_2 = order(dq_2).reg(z, order(dq_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                a_2,
                err_msg="g1 and F3 coefficients should be the same, but are not",
            )


# Note: graph is there to find out what is wrong with gluon VV and why it doesn't follow the relations in the thesis

# def test_cg_NNLO_graph():
#     Q2 = 200
#     esf1 = MockESF("g1_charm", 0.1, Q2)
#     esf2 = MockESF("F2_charm", 0.1, Q2)
#     m2hq = 2
#     for nf in [3, 4]:
#         fig, axs = plt.subplots(1, 2, figsize=(10, 5))
#         a_1_NLO, a_2_NLO, a_1_NNLO, a_2_NNLO = [], [], [], []
#         y= [1e-1, 1e-2, 1e-3]
#         for z in [1e-1, 1e-2, 1e-3]:
#             cg_1 = h_g1_nc.GluonVV(esf1, nf, m2hq=m2hq)
#             cg_2 =  h_f2_nc.GluonVV(esf2, nf, m2hq=m2hq)
#             for o in ["NLO", "NNLO"]:
#                 order = lambda pc, o=o: pc.__getattribute__(o)()
#                 a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
#                 a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
#                 if o == "NLO":
#                     a_1_NLO.append(a_1)
#                     a_2_NLO.append(-a_2)
#                 elif o == "NNLO":
#                     a_1_NNLO.append(a_1)
#                     a_2_NNLO.append(-a_2)
#         axs[0].plot(y, a_1_NLO, color='red', label= 'g1')
#         axs[0].plot(y, a_2_NLO, color='green', label = 'F2')
#         axs[0].set_title('NLO')
#         axs[0].set_xlabel('z')
#         axs[0].set_ylabel('coefficient values')

#         axs[1].plot(y, a_1_NNLO, color='red', label= 'g1')
#         axs[1].plot(y, a_2_NNLO, color='green', label= 'F2')
#         axs[1].set_title('NNLO')
#         axs[1].set_xlabel('z')
#         axs[1].set_ylabel('coefficient values')
#         plt.legend()
#         plt.savefig(f"nf={nf} leading and next to leading order ")
