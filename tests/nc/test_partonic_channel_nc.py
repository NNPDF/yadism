import pytest
import numpy as np
import scipy.integrate

from yadism.nc.partonic_channel import PartonicChannelHeavy

M2hq = 1.0


class MockSF:
    def __init__(self):
        self.M2hq = M2hq


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2


class TestPartonicChannel:
    def test_is_below_threshold(self):

        for Q2 in [0.1, 1000]:
            x = 0.5 
            pch = PartonicChannelHeavy(MockESF(x, Q2), m2hq=M2hq)
            assert pch.decorator( lambda: Q2 )() == np.heaviside(Q2-M2hq, Q2) * Q2