# -*- coding: utf-8 -*-
import numpy as np
import pytest

import yadism.structure_functions.TMC as TMC
from yadism.structure_functions.ESFResult import ESFResult

from eko.interpolation import InterpolatorDispatcher


class MockESF:  # return init arguments
    def __init__(self, q, g=None):
        if g is None:
            g = q[:]
        assert len(q) == len(g)
        self._q = q
        self._g = g

    def get_result(self):
        return ESFResult.from_dict(
            {
                "x": 0,
                "Q2": 0,
                "q": np.array(self._q),
                "g": np.array(self._g),
                "q_error": np.zeros(len(self._q)),
                "g_error": np.zeros(len(self._g)),
            }
        )


class MockTMC(TMC.EvaluatedStructureFunctionTMC):
    # fake abstract methods
    def _get_result_APFEL(self):
        pass

    def _get_result_approx(self):
        pass

    def _get_result_exact(self):
        pass


@pytest.mark.quick_check
class TestTMC:
    @pytest.mark.eko
    def test_convolute_F2_empty(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF:
            _name = "F2light"
            _M2target = 1.0
            _interpolator = InterpolatorDispatcher(xg, 1, False, False, False)

            def get_ESF(self, _name, kinematics):
                # this means F2(x>.6) = 0
                if kinematics["x"] >= 0.6:
                    return MockESF([0.0, 0.0, 0.0])
                return MockESF([1e1, 1e2, 1e3])

        def is0(res):
            assert pytest.approx(res.q, 0, 0) == [0] * 3
            assert pytest.approx(res.g, 0, 0) == [0] * 3
            assert pytest.approx(res.q_error, 0, 0) == [0] * 3
            assert pytest.approx(res.g_error, 0, 0) == [0] * 3

        # build objects
        objSF = MockSF()
        obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
        # test 0 function
        res = obj._convolute_F2(lambda x: 0)
        is0(res)
        # test constant function
        res = obj._convolute_F2(lambda x: 1)
        is0(res)
        # test random function
        res = obj._convolute_F2(np.exp)
        is0(res)
        # test h2
        res = obj._h2()
        is0(res)

    @pytest.mark.eko
    def test_convolute_F2_delta(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF:
            _name = "F2light"
            _M2target = 1.0
            _interpolator = InterpolatorDispatcher(xg, 1, False, False, False)

            def get_ESF(self, _name, kinematics):
                # this means F2 = pdf
                if kinematics["x"] == 0.2:
                    return MockESF([1, 0, 0])
                if kinematics["x"] == 0.6:
                    return MockESF([0, 1, 0])
                if kinematics["x"] == 1.0:
                    return MockESF([0, 0, 1])
                raise ValueError("unkown x")

        # build objects
        objSF = MockSF()
        obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
        # convolute with constant function
        # res_const = int_xi^1 du/u 1 F2(u)
        res_const = obj._convolute_F2(lambda x: 1)
        # res_h2 = int_xi^1 du/u 1/xi*(xi/u) F2(u)  = int_xi^1 du/u 1/u F2(u)
        res_h2 = obj._h2()

        def isdelta(pdf):  # assert F2 = pdf
            for x, pdf_val in zip(xg, pdf):
                ESF_F2 = objSF.get_ESF("", {"x": x, "Q2": 1})
                F2 = np.matmul(ESF_F2.get_result().q, pdf)
                assert pytest.approx(F2) == pdf_val

        # use F2 = pdf = c
        for c in [0.1, 1.0]:
            pdf_const = c * np.array([1, 1, 1])
            isdelta(pdf_const)
            # int_const = int_xi^1 du/u = -ln(xi)
            integral_with_pdf = np.matmul(res_const.q, pdf_const)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (
                -np.log(obj._xi)
            )
            # int_h2 = int_xi^1 du/u^2 = -1 + 1/xi
            integral_with_pdf = np.matmul(res_h2.q, pdf_const)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (
                -1.0 + 1.0 / obj._xi
            )

        # use F2 = pdf = c*x
        for c in [0.5, 1.0]:
            pdf_lin = c * xg
            isdelta(pdf_lin)
            # int_const = int_xi^1 du = 1-xi
            integral_with_pdf = np.matmul(res_const.q, pdf_lin)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (1.0 - obj._xi)
            # int_h2 = int_xi^1 du/u = -ln(xi)
            integral_with_pdf = np.matmul(res_h2.q, pdf_lin)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (
                -np.log(obj._xi)
            )

    @pytest.mark.eko
    def test_convolute_F2_xi_of_domain(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF:
            _name = "F2light"
            _M2target = 1.0
            _interpolator = InterpolatorDispatcher(xg, 1, False, False, False)

            def get_ESF(self, _name, kinematics):
                pass

        # build objects
        objSF = MockSF()
        obj = MockTMC(objSF, {"x": 0.2, "Q2": 1})
        # xi < x so this has to fail
        with pytest.raises(ValueError):
            obj._h2()
