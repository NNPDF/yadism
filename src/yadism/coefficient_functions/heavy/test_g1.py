# -*- coding: utf-8 -*-
import numpy as np
from eko.thresholds import ThresholdsAtlas

from yadism import observable_name as on
from yadism.coefficient_functions.heavy import g1_nc as h_g1_nc 

class MockCouplingConstants:
    def get_weight(self, _pid, _q2, qct):
        if qct == "VV":
            return 1
        if qct == "VA": #-->  must be 0 due to symmetry reasons 
            return 2
        if qct == "AV": #-->  must be 0 due to symmetry reasons 
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
            cg_2 =  h_g1_nc.GluonAA(esf, nf, m2hq=m2hq)
            for o in ["NLO", "NNLO"]:
                order = lambda pc, o=o: pc.__getattribute__(o)()
                a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
                a_2 = order(cg_2).reg(z, order(cg_1).args["reg"])
                print(a_1, a_2, o)
 #todo: test_cg() requires the FONLL method for g1 to compare values? 


def test_cg_NLO():
    Q2 = 200
    esf = MockESF("g1_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg_1 = h_g1_nc.GluonVV(esf, nf, m2hq=m2hq)
            cg_2 =  h_g1_nc.GluonAA(esf, nf, m2hq=m2hq)
            order = lambda pc, o="NLO": pc.__getattribute__("NLO")()
            a_1 = order(cg_1).reg(z, order(cg_1).args["reg"])
            a_2 = order(cg_2).reg(z, order(cg_1).args["reg"])
            np.testing.assert_allclose(a_1, a_2, err_msg='Axial vector-axial vector Coefficients and vector-vector coefficients should be the same, but are not')            


#todo: add tests that compare the poalrized to unpolarized parts to see if they are the same (where they should be)