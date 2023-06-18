import numpy as np

from yadism.coefficient_functions.fonll import f2_nc as f_f2_nc
from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc

from .utils import MockESF


def test_cg():
    Q2 = 200
    esf = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg = h_f2_nc.GluonVV(esf, nf, m2hq=m2hq)
            cgasys = [
                f_f2_nc.AsyLLGluon(esf, nf, m2hq=m2hq),
                f_f2_nc.AsyNLLGluon(esf, nf, m2hq=m2hq),
                f_f2_nc.AsyNNLLGluon(esf, nf, m2hq=m2hq),
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
