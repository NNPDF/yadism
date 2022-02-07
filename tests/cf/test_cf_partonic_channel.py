# -*- coding: utf-8 -*-
import numpy as np
import pytest
import scipy.integrate

from yadism.coefficient_functions import partonic_channel as pc
from yadism.coefficient_functions.heavy import partonic_channel as pcheavy

M2hq = 1.0


class MockSF:
    def __init__(self):
        self.M2hq = M2hq


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2


class TestNeutralCurrentBase:
    def test_is_below_threshold(self):

        for Q2 in [0.1, 1000]:
            x = 0.5
            pch = pcheavy.NeutralCurrentBase(MockESF(x, Q2), 3, m2hq=M2hq)
            assert pch.decorator(lambda: pc.RSL(Q2))().reg == (
                Q2 if Q2 > M2hq else None
            )


class TestPartonicChannel:
    def test_r_integral(self):
        def r_kernel(z, Q2):
            l = Q2 / (Q2 + M2hq)
            return np.log(1 - z * l) / (1 - z)

        for Q2 in np.geomspace(1, 100, 3):
            for x in np.geomspace(1e-3, 0.99, 4):
                pch = pcheavy.ChargedCurrentNonSinglet(MockESF(x, Q2), 4, m2hq=M2hq)
                res, err = scipy.integrate.quad(r_kernel, 0, x, args=(Q2,))
                assert pytest.approx(pch.r_integral(x), 1e-8, err) == res

    def test_h_q(self):

        # TODO: Think a more brilliant test!
        Q2 = 1
        x = 0.5
        pch = pcheavy.ChargedCurrentNonSinglet(MockESF(x, Q2), 5, m2hq=M2hq)
        b1 = lambda x: 1
        b2 = lambda x: 1
        a = 1
        rsl = pch.h_q(a, b1, b2)

        assert rsl.reg(x, [3]) != 0.0
        assert rsl.sing(x, [3]) != 0.0
        assert rsl.loc(x, [3]) != 0.0

    def test_h_g(self):

        # TODO: Think a more brilliant test!
        Q2 = 1
        x = 0.5
        pch = pcheavy.ChargedCurrentGluon(MockESF(x, Q2), 6, m2hq=M2hq)
        cs = [1, 2, 3, 4]
        assert pch.h_g(x, cs) != 0.0
