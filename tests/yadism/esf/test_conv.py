# -*- coding: utf-8 -*-
"""
Test the DistributionVec class and its methods.
"""
import numpy as np
import pytest
from eko.interpolation import InterpolatorDispatcher

from yadism.esf import conv


@pytest.mark.quick_check
@pytest.mark.skip
class TestConvnd:
    @staticmethod
    def against_known_grid(xs, f, coeff, res):
        for x, y in zip(xs, res):
            assert (
                pytest.approx(y, 1 / 1000.0)
                == conv.DistributionVec(*coeff).convolution(x, f)[0]
            )

    @staticmethod
    def against_known(x, f, coeff, res):
        assert (
            pytest.approx(res(x), 1 / 1000.0)
            == conv.DistributionVec(*coeff).convolution(x, f)[0]
        )

    def test_regular(self):
        # format: 3-lists
        # - f: pdf function
        # - coeff: coefficient function (regular bit only, assume the others are 0)
        # - res: results from Mathematica
        known_tests = [[lambda x: x, lambda x: 1, lambda y: 1 - y]]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            test[1] = [test[1]]
            for x in xs:
                self.against_known(x, *test)

    # @pytest.mark.skip
    def test_delta(self):
        # format: 3-lists
        # - f: pdf function
        # - coeff: coefficient function (delta bit only, assume the others are 0)
        # - res: results from Mathematica
        known_tests = [[lambda x: x, lambda x: 1, lambda y: y]]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            # insert missing 0s in coeff func
            test[1] = [lambda x: 0, lambda x: 0, test[1]]
            for x in xs:
                self.against_known(x, *test)

    # @pytest.mark.skip
    def test_pd(self):
        # format: 3-lists
        # - f: pdf function
        # - coeff: coefficient function (pd bit only, assume the others are 0)
        # - res: results from Mathematica
        known_tests = [
            [lambda x: 1, lambda x: 1, lambda y: np.log((1 - y) / y)],
            [lambda x: 1, lambda x: x, lambda y: np.log(1 - y)],
        ]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            # insert missing 0s in coeff func
            test[1] = [lambda x: 0, lambda x: 0, test[2]]
            for x in xs:
                self.against_known(x, *test)

    # @pytest.mark.skip
    def test_log_pd(self):
        # format: 3-lists
        # - f: pdf function
        # - coeff: coefficient function (log_pd bit only, assume the others are 0)
        # - res: results from Mathematica
        # known_tests = [[
        #        lambda x: 1,
        #        lambda y: 1,
        #        np.array([-1.40903, -1.06518, -0.497553, 0.725006]),
        #    ]
        # ]
        known_tests = [
            [lambda x: 1, lambda y: y, np.array([-1.40903])],
            [lambda x: 1, lambda y: y, np.array([-1.06518])],
            [lambda x: 1, lambda y: y, np.array([-0.497553])],
            [lambda x: 1, lambda y: y, np.array([0.725006])],
        ]
        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            # insert missing 0s in coeff func
            test[1] = [lambda x: 0, lambda x: 0, test[2]]
            self.against_known_grid(xs, *test)

    def test_symmetric_conv(self):
        x = 0.4

        kmas = [
            [lambda x: 1, lambda x: 0, lambda x: 0, lambda x: 0],
            [lambda x: x, lambda x: 0, lambda x: 0, lambda x: 0],
        ]
        fs = [lambda x: x, lambda x: 1]

        results = []
        for f, kma in zip(fs, kmas):
            results.append(conv.DistributionVec(kma).convolution(x, f)[0])

        assert pytest.approx(results[0], 1 / 1000.0) == results[1]

    @pytest.mark.eko
    def test_basis_function_void(self):
        xg = np.linspace(0.2, 1.0, 5)  # 0.2, 0.4, 0.6, 0.8, 1.0
        i = InterpolatorDispatcher(xg, 1, False)
        bf1 = i[0]  # ranges from 0.2 to 0.4
        # they should give the same result
        for x in [0.4, 0.5, 0.6]:  # quad should never trigger
            d = conv.DistributionVec(lambda z: z)
            res = d.convolution(x, bf1)
            assert res[0] == 0.0
            assert res[1] == 0.0

    @pytest.mark.eko
    def test_basis_function_shrink_domain_lin(self):
        xg = np.linspace(0.2, 1.0, 5)  # 0.2, 0.4, 0.6, 0.8, 1.0
        i = InterpolatorDispatcher(xg, 1, False)
        # fake eko and test it does the job
        def bf1(x):
            if x > 0.4:
                return 0.0
            return (0.4 - x) / 0.2

        true_bf1 = i[0]
        for y in np.linspace(0.2, 0.5, 100):
            assert pytest.approx(bf1(y), 1 / 1000.0) == true_bf1(y)
        # they should give the same result
        for x in [0.2, 0.3, 0.4, 0.5]:
            for d in [
                conv.DistributionVec(lambda z: z),
                conv.DistributionVec(0, 1),
                conv.DistributionVec(0, 0, 1),
            ]:
                res = d.convolution(x, bf1)
                true_res = d.convolution(x, true_bf1)
                assert pytest.approx(res[0], 1 / 1000.0) == true_res[0]

    @pytest.mark.eko
    def test_basis_function_shrink_domain_log(self):
        xg = np.array([np.exp(-2), np.exp(-1), 1.0])
        i = InterpolatorDispatcher(xg, 1, True)
        # fake eko and test it does the job
        def bf1(x):
            if np.log(x) > -1:
                return 0.0
            return -1 - np.log(x)

        true_bf1 = i[0]
        for y in np.linspace(np.exp(-2), 1.0, 100):
            assert pytest.approx(bf1(y), 1 / 1000.0) == true_bf1(y)
        # they should give the same result
        for x in np.exp([-2.0, -1.5, -1.0, -0.5, 0.0]):
            for d in [
                conv.DistributionVec(lambda z: z),
                conv.DistributionVec(0, 1),
                conv.DistributionVec(0, 0, 1),
            ]:
                res = d.convolution(x, bf1)
                true_res = d.convolution(x, true_bf1)
                assert pytest.approx(res[0], 1 / 1000.0) == true_res[0]

    def test_conv_zero(self):
        dvec0 = conv.DistributionVec(None, 0, None)
        dvec1 = conv.DistributionVec(None, None, None)
        f = lambda x: 1
        for x in np.exp([-2.0, -1.5, -1.0, -0.5, 0.0]):
            assert dvec0.convolution(x, f) == (0, 0)
            assert dvec1.convolution(x, f) == (0, 0)
