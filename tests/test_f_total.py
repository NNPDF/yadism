# -*- coding: utf-8 -*-
import copy

from yadism import observable_name
from yadism.structure_functions.nc import f_total
from yadism.structure_functions import esf_result


class MockInterpolator:
    xgrid_raw = [0.01, 0.1]


class MockESF:
    def __init__(self, res):
        self.res = res

    def get_result(self):
        return self.res


class MockPDFdonly:
    def xfxQ2(self, pid, _x, _Q2):
        if pid == 1:
            return 1.0  # it is xfxQ2! beware of the additional x
        return 0


class MockSF:
    obs_name = observable_name.ObservableName("F2total")
    interpolator = MockInterpolator()

    def get_esf(self, obs_name, kinematics, **_kwargs):
        src = copy.deepcopy(kinematics)
        if obs_name.name == "F2light":
            src.update(
                {"values": {"q": [1]}, "errors": {"q": [0]}, "weights": {"q": {1: 1}}}
            )
            return MockESF(esf_result.ESFResult.from_dict(src))
        if obs_name.name == "F2charm":
            src.update(
                {"values": {"q": [2]}, "errors": {"q": [0]}, "weights": {"q": {1: 2}}}
            )
            return MockESF(esf_result.ESFResult.from_dict(src))
        src.update({"values": {}, "errors": {}, "weights": {}})
        return MockESF(esf_result.ESFResult.from_dict(src))


class TestFtotal:
    def test_combine(self):
        sf = MockSF()
        o = f_total.EvaluatedStructureFunctionFtotal(sf, {"x": 0.1, "Q2": 10})
        res = o.get_result()
        # check ingredients
        assert tuple(res.values.keys()) == ("q_total_light", "q_total_charm")
        assert res.values["q_total_light"] == [1]
        assert res.values["q_total_charm"] == [2]
        # check apply pdf
        out = res.apply_pdf([1], 1.0, MockPDFdonly())
        assert out["result"] == 1 * 1 * 1 + 1 * 2 * 2
        assert out["error"] == 0
