# -*- coding: utf-8 -*-
"""
Test all the partonic coefficient functions
"""
import numpy as np

from yadism import cc

M2hq = 1.0

class MockSF:
    def __init__(self):
        #self.M2hq = M2hq
        pass


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2

# class TestF2asy:

#     def test_quark(self):
#         x = 0.9
#         Q2 = 10
#         f2asy_q = cc.f2_asy.F2asyQuark(MockESF(x, Q2), m2hq = M2hq)
#         assert f2asy_q.LO()[2] == 1
#         for i in range(2):
#             assert type(f2asy_q.NLO()[i](x)) == py.float64
#             assert type(f2asy_q.NLO_fact()[i](x)) == float


#     def test_gluon(self):
#         x = 0.9
#         Q2 = 10
#         f2asy_g = cc.f2_asy.F2asyGluon(MockESF(x, Q2), m2hq = M2hq)
#         assert type(f2asy_g.NLO()(x)) == py.float64
#         assert type(f2asy_g.NLO_fact()(x)) == float


class TestHeavy:

    def test_quark(self):
        x = 0.9
        Q2 = 10
        z = x

        for pc in [cc.f2_heavy.F2heavyQuark(MockESF(x, Q2), m2hq = M2hq),cc.f3_heavy.F3heavyQuark(MockESF(x, Q2), m2hq = M2hq),cc.fl_heavy.FLheavyQuark(MockESF(x, Q2), m2hq = M2hq)]:
            assert pc.LO()[0] == 0
            assert pc.LO()[1] == 0
            assert isinstance(pc.LO()[2],float)
            for i in range(2):
                assert isinstance(pc.NLO()[i](z),float)
                assert isinstance(pc.NLO_fact()[i](z), float)


    def test_gluon(self):
        x = 0.9
        Q2 = 10
        z = x
        for pc in [cc.f2_heavy.F2heavyGluon(MockESF(x, Q2), m2hq = M2hq),cc.f3_heavy.F3heavyGluon(MockESF(x, Q2), m2hq = M2hq),cc.fl_heavy.FLheavyGluon(MockESF(x, Q2), m2hq = M2hq)]:
            assert pc.LO() == None
            assert isinstance(pc.NLO()(z),float)
            assert isinstance(pc.NLO_fact()(z), float)
