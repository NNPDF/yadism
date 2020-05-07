# -*- coding: utf-8 -*-
import numpy as np
import pytest

import yadism.structure_functions.TMC as TMC

from eko.interpolation import InterpolatorDispatcher

class TestTMC:
    def test_integrate_F2_empty(self):
        xg = [0.2, 0.6, 1.0]
        # return init argument
        class MockESF:
            def __init__(self, q, g=None):
                if g is None:
                    g = q[:]
                assert len(q) == len(g)
                self._q = q
                self._g = g
            def get_output(self):
                return {
                    "q": np.array(self._q),
                    "g": np.array(self._g),
                    "q_error": np.zeros(len(self._q)),
                    "g_error": np.zeros(len(self._g)),
                }

        class MockSF:
            _name = "F2light"
            _M2target = 1.0
            _interpolator = InterpolatorDispatcher(xg,1,False,False,False)
            def get_ESF(self, name, kinematics):
                # this means F2(x>.6) = 0
                if kinematics["x"] >= 0.6:
                    return MockESF([0,0,0])
                return MockESF([1e1,1e2,1e3])
        
        # fake abstract methods
        class MockTMC(TMC.EvaluatedStructureFunctionTMC):
            def _get_output_APFEL(self): pass
            def _get_output_approx(self): pass
            def _get_output_exact(self): pass

        # build objects
        objSF = MockSF()
        obj = MockTMC(objSF,{"x":0.99,"Q2":1})
        # test 0 function
        res = obj._integrate_F2(lambda x: 0)
        assert pytest.approx(res["q"],0,0) == [0]*3
        assert pytest.approx(res["g"],0,0) == [0]*3
        # test constant function
        res = obj._integrate_F2(lambda x: 1)
        assert pytest.approx(res["q"],0,0) == [0]*3
        assert pytest.approx(res["g"],0,0) == [0]*3
        # test random function
        res = obj._integrate_F2(lambda x: np.exp(x))
        assert pytest.approx(res["q"],0,0) == [0]*3
        assert pytest.approx(res["g"],0,0) == [0]*3
