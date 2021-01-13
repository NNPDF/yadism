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
        self._x = x
        self._Q2 = q2


class TestPartonicChannel:
    pass
