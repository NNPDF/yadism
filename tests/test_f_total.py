# -*- coding: utf-8 -*-
import copy

#import numpy as np
#import pytest

from yadism.structure_functions import f_total
from yadism.structure_functions import esf_result

class MockInterpolator:
    xgrid_raw = [0.01, 0.1]

class MockESF:
    def __init__(self,res):
        self.res = res
    def get_result(self):
        return self.res

class MockPDFdonly:
    def xfxQ2(self, pid, x, Q2):
        if pid == 1:
            return 1.  # it is xfxQ2! beware of the additional x
        return 0

class MockSF:
    name = "F2total"
    interpolator = MockInterpolator()

    def get_esf(self, name, kinematics):
        src = copy.deepcopy(kinematics)
        if name == "F2light":
            src.update({"values":{"q":[1]},"errors":{"q":[0]},"weights":{"q":{1:1}}})
            return MockESF(esf_result.ESFResult.from_dict(src))
        if name == "F2charm":
            src.update({"values":{"q":[2]},"errors":{"q":[0]},"weights":{"q":{1:2}}})
            return MockESF(esf_result.ESFResult.from_dict(src))
        src.update({"values":{},"errors":{},"weights":{}})
        return MockESF(esf_result.ESFResult.from_dict(src))

class TestFtotal:
    def test_combine(self):
        sf = MockSF()
        o = f_total.EvaluatedStructureFunctionFtotal(sf,{"x":.1, "Q2": 10})
        res = o.get_result()
        # check ingredients
        assert tuple(res.values.keys()) == ("qlight","qcharm")
        assert res.values["qlight"] == [1]
        assert res.values["qcharm"] == [2]
        # check apply pdf
        out = res.apply_pdf([1],1.,MockPDFdonly())
        assert out["result"] == 1 * 1 * 1 + 1*2*2
        assert out["error"] == 0