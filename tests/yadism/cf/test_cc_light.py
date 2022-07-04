# -*- coding: utf-8 -*-
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
