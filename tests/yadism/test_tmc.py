# -*- coding: utf-8 -*-
import copy

import numpy as np
import pytest
from eko.interpolation import InterpolatorDispatcher

import yadism.esf.tmc as TMC
from yadism import observable_name
from yadism.esf.result import ESFResult

lo = (0, 0, 0, 0)


class MockESF:
    def __init__(self, vals):
        self.res = ESFResult(0.1, 10, nf=3)
        self.res.orders[lo] = (np.array([vals]), np.zeros(len(vals)))

    def get_result(self):
        return copy.deepcopy(self.res)


class MockTMC(TMC.EvaluatedStructureFunctionTMC):
    # fake abstract methods
    def _get_result_APFEL(self):
        return MockESF([1.0, 0.0, 0.0])

    def _get_result_approx(self):
        return MockESF([2.0, 0.0, 0.0])

    def _get_result_exact(self):
        return MockESF([3.0, 0.0, 0.0])


class MockObj:
    pass


class MockSF:
    obs_name = observable_name.ObservableName("F2_light")

    def __init__(self, tmc, xg=None):
        if xg is None:
            xg = np.array([0.2, 0.6, 1.0])
        self.runner = MockObj()
        self.runner.configs = MockObj()
        self.runner.configs.M2target = 1.0
        self.runner.configs.TMC = tmc
        self.runner.configs.interpolator = InterpolatorDispatcher(xg, 1, False, False)


class TestAbstractTMC:
    def test_mode(self):
        for k in [1, 2, 3]:
            objSF = MockSF(k)
            obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
            esf = obj.get_result()
            np.testing.assert_allclose(esf.get_result().orders[lo][0][0][0], k)

        # no TMC active
        with pytest.raises(RuntimeError):
            objSF = MockSF(0)
            obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
            obj.get_result()
        # unknown TMC active
        with pytest.raises(ValueError):
            objSF = MockSF(-1)
            obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
            obj.get_result()

    def test_convolute_F2_empty(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF1(MockSF):
            def get_esf(self, _name, kinematics):
                # this means F2(x>.6) = 0
                if kinematics["x"] >= 0.6:
                    return MockESF([0.0, 0.0, 0.0])
                return MockESF([1e1, 1e2, 1e3])

        # is empty
        def is0(res):
            np.testing.assert_allclose(np.max(np.abs(res.orders[lo][0])), 0)
            np.testing.assert_allclose(np.max(np.abs(res.orders[lo][1])), 0)

        # build objects
        objSF = MockSF1(1, xg)
        obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
        # test 0 function
        res = obj._convolute_FX(  # pylint: disable=protected-access
            "F2", lambda _x, _args: 0
        )
        is0(res)
        # test constant function
        res = obj._convolute_FX(  # pylint: disable=protected-access
            "F2", lambda _x, _args: 1
        )
        is0(res)
        # test random function
        res = obj._convolute_FX("F2", np.exp)  # pylint: disable=protected-access
        is0(res)
        # test h2
        res = obj._h2()  # pylint: disable=protected-access
        is0(res)
        # test g2
        res = obj._g2()  # pylint: disable=protected-access
        is0(res)

    def test_convolute_F2_delta(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF2(MockSF):
            def get_esf(self, _name, kinematics):
                # this means F2 = pdf
                if kinematics["x"] == 0.2:
                    return MockESF([1, 0, 0])
                if kinematics["x"] == 0.6:
                    return MockESF([0, 1, 0])
                if kinematics["x"] == 1.0:
                    return MockESF([0, 0, 1])
                raise ValueError("unkown x")

        # build objects
        objSF = MockSF2(1, xg)
        obj = MockTMC(objSF, {"x": 0.99, "Q2": 1})
        # convolute with constant function
        # res_const = int_xi^1 du/u 1 F2(u)
        res_const = obj._convolute_FX(  # pylint: disable=protected-access
            "F2", lambda x, args: 1
        )
        assert isinstance(res_const, ESFResult)
        # res_h2 = int_xi^1 du/u 1/xi*(xi/u) F2(u)  = int_xi^1 du/u 1/u F2(u)
        res_h2 = obj._h2()  # pylint: disable=protected-access
        assert isinstance(res_h2, ESFResult)

        def isdelta(pdf):  # assert F2 = pdf
            for x, pdf_val in zip(xg, pdf):
                ESF_F2 = objSF.get_esf("", {"x": x, "Q2": 1})
                F2 = np.matmul(ESF_F2.get_result().orders[lo][0][0], pdf)
                assert pytest.approx(F2) == pdf_val

        # use F2 = pdf = c
        for c in [0.1, 1.0]:
            pdf_const = c * np.array([1, 1, 1])
            isdelta(pdf_const)
            # int_const = int_xi^1 du/u = -ln(xi)
            integral_with_pdf = np.matmul(res_const.orders[lo][0][0], pdf_const)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (-np.log(obj.xi))
            # int_h2 = int_xi^1 du/u^2 = -1 + 1/xi
            integral_with_pdf = np.matmul(res_h2.orders[lo][0][0], pdf_const)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (
                -1.0 + 1.0 / obj.xi
            )

        # use F2 = pdf = c*x
        for c in [0.5, 1.0]:
            pdf_lin = c * xg
            isdelta(pdf_lin)
            # int_const = int_xi^1 du = 1-xi
            integral_with_pdf = np.matmul(res_const.orders[lo][0][0], pdf_lin)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (1.0 - obj.xi)
            # int_h2 = int_xi^1 du/u = -ln(xi)
            integral_with_pdf = np.matmul(res_h2.orders[lo][0][0], pdf_lin)
            assert pytest.approx(integral_with_pdf, 1 / 1000.0) == c * (-np.log(obj.xi))

    def test_convolute_F2_xi_of_domain(self):
        xg = np.array([0.2, 0.6, 1.0])

        class MockSF3(MockSF):
            def get_esf(self, _name, kinematics):
                pass

        #  build objects
        objSF = MockSF3(1, xg)
        obj = MockTMC(objSF, {"x": 0.2, "Q2": 1})
        #  xi < x so this has to fail
        with pytest.raises(ValueError):
            obj._h2()  # pylint: disable=protected-access
