# -*- coding: utf-8 -*-
"""
Test all the partonic coefficient functions
"""

from yadism.coefficient_functions.light import (
    f2_cc as lf2cc,
    fl_cc as lflcc,
    f3_cc as lf3cc,
    f2_nc as lf2nc,
    fl_nc as lflnc,
    f3_nc as lf3nc,
)
from yadism.coefficient_functions.heavy import (
    f2_cc as hf2cc,
    fl_cc as hflcc,
    f3_cc as hf3cc,
    f2_nc as hf2nc,
    fl_nc as hflnc,
)
from yadism.coefficient_functions.fonll import (
    f2_nc as af2nc,
    fl_nc as aflnc,
    f2_cc as af2cc,
    fl_cc as aflcc,
    f3_cc as af3cc,
)
from yadism.coefficient_functions.intrinsic import (
    f2_nc as if2nc,
    fl_nc as iflnc,
    f3_nc as if3nc,
)

M2hq = 1.0
nf = 3


class MockSF:
    pass


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2


class TestFloat:
    def test_quark(self):
        x = 0.1
        Q2 = 10
        z = x

        # non trivial LO + NLO*
        for pc in [
            hf2cc.NonSinglet(MockESF(x, Q2), m2hq=M2hq),
            hf3cc.NonSinglet(MockESF(x, Q2), m2hq=M2hq),
            hflcc.NonSinglet(MockESF(x, Q2), m2hq=M2hq),
            af2cc.AsyQuark(MockESF(x, Q2), mu2hq=M2hq),
            af3cc.AsyQuark(MockESF(x, Q2), mu2hq=M2hq),
            lf2cc.NonSinglet(MockESF(x, Q2), nf=nf),
            lf3cc.NonSinglet(MockESF(x, Q2), nf=nf),
            lf2nc.NonSinglet(MockESF(x, Q2), nf=nf),
            lf3nc.NonSinglet(MockESF(x, Q2), nf=nf),
        ]:
            assert pc.LO()[0] == 0
            assert pc.LO()[1] == 0
            assert isinstance(pc.LO()[2], float)
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)
                assert isinstance(pc.NLO_fact()[i](z), float)

        # LO=0
        for pc in [
            aflcc.AsyQuark(MockESF(x, Q2), mu2hq=M2hq),
            lflcc.NonSinglet(MockESF(x, Q2), nf=nf),
        ]:
            assert pc.LO() is None
            assert isinstance(pc.NLO()(z), float)
            assert pc.NLO_fact() is None

    def test_gluon(self):
        x = 0.1
        Q2 = 10
        for z in [x, 0.9]:
            # non trivial LO + NLO*
            for pc in [
                af2cc.AsyGluon(MockESF(x, Q2), mu2hq=M2hq),
                af3cc.AsyGluon(MockESF(x, Q2), mu2hq=M2hq),
                hf2cc.Gluon(MockESF(x, Q2), m2hq=M2hq),
                hf3cc.Gluon(MockESF(x, Q2), m2hq=M2hq),
                hflcc.Gluon(MockESF(x, Q2), m2hq=M2hq),
                lf2cc.Gluon(MockESF(x, Q2), nf=nf),
            ]:
                assert pc.LO() is None
                assert isinstance(pc.NLO()(z), float)
                assert isinstance(pc.NLO_fact()(z), float)

            # LO=0
            for pc in [
                lflcc.Gluon(MockESF(x, Q2), nf=nf),
                aflcc.AsyGluon(MockESF(x, Q2), mu2hq=M2hq),
                lflnc.Gluon(MockESF(x, Q2), nf=nf),
                af2nc.AsyGluonVV(MockESF(x, Q2), mu2hq=M2hq),
                af2nc.AsyGluonAA(MockESF(x, Q2), mu2hq=M2hq),
                aflnc.AsyGluonVV(MockESF(x, Q2), mu2hq=M2hq),
                aflnc.AsyGluonAA(MockESF(x, Q2), mu2hq=M2hq),
                hf2nc.GluonVV(MockESF(x, Q2), m2hq=M2hq),
                hf2nc.GluonAA(MockESF(x, Q2), m2hq=M2hq),
                hflnc.GluonVV(MockESF(x, Q2), m2hq=M2hq),
                hflnc.GluonAA(MockESF(x, Q2), m2hq=M2hq),
            ]:
                assert pc.LO() is None
                assert isinstance(pc.NLO()(z), float)
                assert pc.NLO_fact() is None


class TestIntrisic:
    def test_quark(self):
        x = 0.1
        Q2 = 10
        z = x

        # non trivial LO + NLO*
        for pc in [
            if2nc.Splus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            iflnc.Splus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            iflnc.Sminus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            if3nc.Rplus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO()[0] == 0
            assert pc.LO()[1] == 0
            assert isinstance(pc.LO()[2], float)
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)

        # LO=0
        for pc in [
            if2nc.Sminus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            if3nc.Rminus(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO() is None
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)
