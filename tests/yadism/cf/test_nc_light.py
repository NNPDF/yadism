# -*- coding: utf-8 -*-
from test_pc_general import MockESF

from yadism.coefficient_functions.light import f2_nc, fl_nc


def test_N3LO_labels():
    Q2 = 200
    x = 0.1
    esf = MockESF(x, Q2)
    nf = 3
    fl_ns = fl_nc.NonSinglet(esf, nf)
    f2_ns = f2_nc.NonSinglet(esf, nf)

    assert fl_ns.N3LO().args["reg"] is not None
    assert fl_ns.N3LO().args["loc"] is not None
    assert f2_ns.N3LO().args["reg"] is not None
    assert f2_ns.N3LO().args["loc"] is not None
    assert f2_ns.N3LO().args["sing"] is not None

    fl_g = fl_nc.Gluon(esf, nf)
    f2_g = f2_nc.Gluon(esf, nf)

    assert fl_g.N3LO().args["reg"] is not None
    assert f2_g.N3LO().args["reg"] is not None
    assert f2_g.N3LO().args["loc"] is not None

    fl_s = fl_nc.Singlet(esf, nf)
    f2_s = f2_nc.Singlet(esf, nf)

    assert fl_s.N3LO().args["reg"] is not None
    assert f2_s.N3LO().args["reg"] is not None
    assert f2_s.N3LO().args["loc"] is not None
