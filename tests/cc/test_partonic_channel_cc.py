import pytest
import numpy as np
import scipy.integrate

from yadism.cc.partonic_channel import PartonicChannelHeavy

M2hq = 1.0


class MockSF:
    def __init__(self):
        self.M2hq = M2hq


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self._x = x
        self._Q2 = q2


class TestPartonicChannel:
    def test_r_integral(self):
        def r_kernel(z, Q2):
            l = Q2 / (Q2 + M2hq)
            return np.log(1 - z * l) / (1 - z)

        for Q2 in np.geomspace(1, 100, 3):
            for x in np.geomspace(1e-3, 0.99, 4):
                pch = PartonicChannelHeavy(MockESF(x, Q2))
                res, err = scipy.integrate.quad(r_kernel, 0, x, args=(Q2,))
                assert pytest.approx(pch.r_integral(x), 1e-8, err) == res
