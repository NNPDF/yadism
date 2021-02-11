import numpy as np

from yadism.nc import kernels
from yadism import observable_name as on


class MockCouplingConstants:
    def get_weight(self, _pid, _q2, qct):
        if qct == "VV":
            return 1
        if qct == "VA":
            return 2
        if qct == "AV":
            return 4
        if qct == "AA":
            return 8


class MockSF:
    def __init__(self, n):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants()


class MockESF:
    def __init__(self, sf, q2):
        self.sf = MockSF(sf)
        self.Q2 = q2


def test_generate_light():
    esf = MockESF("F2light", 10)
    for nf in [3, 5]:
        w = kernels.generate_light(esf, nf)
        assert len(w[0].partons) == 2 * nf  # ns
        assert len(w[1].partons) == 1  # g
        assert len(w[0].partons) == 2 * nf  # s
