# -*- coding: utf-8 -*-
"""
Test all the partonic coefficient functions
"""

from yadism import cc, nc

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
            cc.f2_heavy.F2heavyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.f3_heavy.F3heavyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.fl_heavy.FLheavyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.f2_asy.F2asyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.f3_asy.F3asyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.f2_light.F2lightQuark(MockESF(x, Q2), nf=nf),
            cc.f3_light.F3lightQuark(MockESF(x, Q2), nf=nf),
            nc.f2_light.F2lightNonSinglet(MockESF(x, Q2), nf=nf),
            nc.f3_light.F3lightNonSinglet(MockESF(x, Q2), nf=nf),
        ]:
            assert pc.LO()[0] == 0
            assert pc.LO()[1] == 0
            assert isinstance(pc.LO()[2], float)
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)
                assert isinstance(pc.NLO_fact()[i](z), float)

        # LO=0
        for pc in [
            cc.fl_asy.FLasyQuark(MockESF(x, Q2), m2hq=M2hq),
            cc.fl_light.FLlightQuark(MockESF(x, Q2), nf=nf),
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
                cc.f2_asy.F2asyGluon(MockESF(x, Q2), m2hq=M2hq),
                cc.f3_asy.F3asyGluon(MockESF(x, Q2), m2hq=M2hq),
                cc.f2_heavy.F2heavyGluon(MockESF(x, Q2), m2hq=M2hq),
                cc.f3_heavy.F3heavyGluon(MockESF(x, Q2), m2hq=M2hq),
                cc.fl_heavy.FLheavyGluon(MockESF(x, Q2), m2hq=M2hq),
                cc.f2_light.F2lightGluon(MockESF(x, Q2), nf=nf),
            ]:
                assert pc.LO() is None
                assert isinstance(pc.NLO()(z), float)
                assert isinstance(pc.NLO_fact()(z), float)

            # LO=0
            for pc in [
                cc.fl_light.FLlightGluon(MockESF(x, Q2), nf=nf),
                cc.fl_asy.FLasyGluon(MockESF(x, Q2), m2hq=M2hq),
                nc.fl_light.FLlightGluon(MockESF(x, Q2), nf=nf),
                nc.f2_asy.F2asyGluonVV(MockESF(x, Q2), m2hq=M2hq),
                nc.f2_asy.F2asyGluonAA(MockESF(x, Q2), m2hq=M2hq),
                nc.fl_asy.FLasyGluonVV(MockESF(x, Q2), m2hq=M2hq),
                nc.fl_asy.FLasyGluonAA(MockESF(x, Q2), m2hq=M2hq),
                nc.f2_heavy.F2heavyGluonVV(MockESF(x, Q2), m2hq=M2hq),
                nc.f2_heavy.F2heavyGluonAA(MockESF(x, Q2), m2hq=M2hq),
                nc.fl_heavy.FLheavyGluonVV(MockESF(x, Q2), m2hq=M2hq),
                nc.fl_heavy.FLheavyGluonAA(MockESF(x, Q2), m2hq=M2hq),
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
            cc.f2_intrinsic.F2IntrinsicSp(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            cc.fl_intrinsic.FLIntrinsicSp(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            nc.fl_intrinsic.FLIntrinsicSm(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            cc.f3_intrinsic.F3IntrinsicRp(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO()[0] == 0
            assert pc.LO()[1] == 0
            assert isinstance(pc.LO()[2], float)
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)

        # LO=0
        for pc in [
            nc.f2_intrinsic.F2IntrinsicSm(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
            nc.f3_intrinsic.F3IntrinsicRm(MockESF(x, Q2), m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO() is None
            for i in range(3):
                assert isinstance(pc.NLO()[i](z), float)
