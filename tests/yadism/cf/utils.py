from eko.matchings import Atlas

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
        raise ValueError(f"Unkown {qct}")


class MockSF:
    def __init__(self, n):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants()
        self.m2hq = [1.0, 2.0, 3.0]
        self.threshold = Atlas(matching_scales=self.m2hq, origin=(1.65**2, 4))


class MockESF:
    def __init__(self, sf, x, Q2):
        self.sf = MockSF(sf)
        self.x = x
        self.Q2 = Q2
        self.process = "NC"
