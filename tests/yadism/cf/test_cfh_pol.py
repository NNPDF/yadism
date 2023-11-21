import numpy as np

from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc
from yadism.coefficient_functions.heavy import f3_nc as h_f3_nc
from yadism.coefficient_functions.heavy import fl_nc as h_fl_nc
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc
from yadism.coefficient_functions.heavy import g4_nc as h_g4_nc
from yadism.coefficient_functions.heavy import gl_nc as h_gl_nc

from .utils import MockESF


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
                err_msg="Gluon VV & AA coefficients at NLO should be the same, but are not",
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


def test_cg_NNLO_NS_glfl():
    Q2 = 200
    esf1 = MockESF("gL_charm", 0.1, Q2)
    esf2 = MockESF("FL_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_gl_nc.NonSinglet(esf1, nf, m2hq=m2hq)
            cg_2 = h_fl_nc.NonSinglet(esf2, nf, m2hq=m2hq)
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
            a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                -a_2,
                err_msg="gL and FL coefficients at NNLO should be the same, but are not",
            )


def test_cg_NNLO_NS_g4f2():
    Q2 = 200
    esf1 = MockESF("g4_charm", 0.1, Q2)
    esf2 = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_g4_nc.NonSinglet(esf1, nf, m2hq=m2hq)
            cg_2 = h_f2_nc.NonSinglet(esf2, nf, m2hq=m2hq)
            order = lambda pc, o="NNLO": pc.__getattribute__("NNLO")()
            a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
            a_2 = order(cg_2).reg(z, order(cg_2).args["reg"])
            np.testing.assert_allclose(
                a_1,
                -a_2,
                err_msg="g4 and F2 coefficients at NNLO should be the same, but are not",
            )
