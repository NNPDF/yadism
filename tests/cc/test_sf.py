# -*- coding: utf-8 -*-
"""
Test all the SF coefficients 
"""

import pytest

import numpy as py

from yadism import cc
from yadism import partonic_channel as pc 

M2hq = 1.0

class MockSF:
    def __init__(self):
        self.M2hq = M2hq


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2

class TestF2asy:
    
    def test_quark(self):
        x = 0.9
        Q2 = 10
        f2asy_q = cc.f2_asy.F2asyQuark(MockESF(x, Q2), m2hq = M2hq)
        assert f2asy_q.LO()[2] == 1
        for i in range(2):
            assert type(f2asy_q.NLO()[i](x)) == py.float64
            assert type(f2asy_q.NLO_fact()[i](x)) == float


    def test_gluon(self):
        x = 0.9
        Q2 = 10
        f2asy_g = cc.f2_asy.F2asyGluon(MockESF(x, Q2), m2hq = M2hq)
        assert type(f2asy_g.NLO()(x)) == py.float64
        assert type(f2asy_g.NLO_fact()(x)) == float


class TestF2heavy:
    
    def test_quark(self):
        x = 0.9
        Q2 = 10
        f2heavy_q = cc.f2_heavy.F2heavyQuark(MockESF(x, Q2), m2hq = M2hq)
        assert f2heavy_q.LO()[2] == 1
        for i in range(2):
            assert type(f2heavy_q.NLO()[i](x)) == py.float64
            assert type(f2heavy_q.NLO_fact()[i](x)) == float


    def test_gluon(self):
        x = 0.9
        Q2 = 10
        f2heavy_g = cc.f2_heavy.F2heavyGluon(MockESF(x, Q2), m2hq = M2hq)
        assert type(f2heavy_g.NLO()(x)) == py.float64
        assert type(f2heavy_g.NLO_fact()(x)) == float