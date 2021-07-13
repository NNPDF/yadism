# -*- coding: utf-8 -*-
"""
Test the DistributionVec class and its methods.
"""
import copy

import numpy as np
import pytest
from eko.interpolation import InterpolatorDispatcher

from yadism.esf import conv


# @pytest.mark.quick_check
# @pytest.mark.skip
class TestInit:
    def test_init_zero(self):
        d_vecs = [
            conv.DistributionVec(None),
            conv.DistributionVec(None, None),
            conv.DistributionVec(None, None, None),
            conv.DistributionVec([None, None]),
        ]

        for d_vec in d_vecs:
            for x in [0.1, 0.3, 0.5, 0.9]:
                for c in d_vec:
                    try:
                        assert c(x) == None
                    except:
                        assert c == None

    def test_init_const(self):
        vecs = [
            [1, 1, 1],
            [1.0, 1.0, 1.0],
            [lambda x: 1, lambda x: 1, lambda x: 1],
            [1, 1, lambda x: 1],
            [
                [
                    1,
                    1,
                    1,
                    1,
                ]
            ],
            [[1, 1, 1, lambda x: 1]],
            [[lambda x: 1, 1, 1, 1]],
        ]

        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            for c in d_vec:
                for x in [0.1, 0.3, 0.5, 0.9]:
                    try:
                        assert c(x) == 1
                    except:
                        assert c == 1

    def test_init_different(self):
        """
        Keep this separate from the previous one because it
        is more involved, since we are not comparing with a
        fixed target.
        """
        vecs = [
            [1, 2, 3],
            [1, lambda x: 2, 103],
            [1, 202, 3],
            [1, None, 3],
            [[1, 2, 3, 4]],
            [[1, 2, 703, lambda x: 4]],
            [[lambda x: 1, 492, 3, 4]],
        ]

        x = 0.5
        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            if isinstance(vec[0], list):
                vec = vec[0]

            for v, c in zip(vec, d_vec):
                if callable(v):
                    vi = v(x)
                elif v is None:
                    vi = 0
                else:
                    vi = float(v)

                    try:
                        assert c(x) == vi
                    except:
                        assert c == vi


# @pytest.mark.quick_check
# @pytest.mark.skip
class TestSpecial:
    def test_rsl_from_distr_coeffs(self):
        regular = [lambda x: x]
        delta = 1
        coeffs = [1, 2, 3]
        res_singular = 0
        res_local = 0
        z = 0.3
        assert regular == conv.rsl_from_distr_coeffs(regular, delta, *coeffs)[0]
        for coeff in coeffs:
            res_singular += coeff * 1 / (1 - z) * np.log(1 - z) ** (coeff - 1)
            res_local += coeff * np.log(1 - z) ** (coeff) / (coeff)

        assert res_singular == conv.rsl_from_distr_coeffs(regular, delta, *coeffs)[1](z)
        assert res_local + delta == conv.rsl_from_distr_coeffs(regular, delta, *coeffs)[
            2
        ](z)

    def test_iter_zero(self):
        vec = [lambda x: x, 1, None]
        d_vec = conv.DistributionVec(*vec)

        i = 0
        for val in d_vec.__iter__():
            assert vec[i] == val
            i = i + 1

    def test_iter(self):
        vecs = [
            [1, 2, 3],
            [1001, 2, 103],
        ]

        x = 0.5
        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            if isinstance(vec[0], list):
                vec = vec[0]

            for i, c in enumerate(d_vec):
                assert vec[i] == c

    def test_add_d_vec(self):
        vecs = [
            [1, 2, 3],
            [1001, 2, 103],
        ]
        vec0 = np.array([2837, 91283, 3897])
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for vec in vecs:
            ref_d_vec = conv.DistributionVec(*(np.array(vec) + vec0))
            sum_d_vec = conv.DistributionVec(*vec) + d_vec0

            assert ref_d_vec.compare(sum_d_vec, x)

    def test_add_func(self):
        fs = [lambda x: 18, lambda x: (1 - x)]

        vec0 = np.array([2837, 91283, 3897], dtype=float)
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for f in fs:
            vec = vec0.copy()
            vec[0] += f(x)
            ref_d_vec = conv.DistributionVec(*vec)
            sum_d_vec = d_vec0 + f(x)

            assert ref_d_vec.compare(sum_d_vec, x)

    def test_add_const(self):
        cs = [1328, -435.421]

        vec0 = np.array([4.45, 2483, 7.452], dtype=float)
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for c in cs:
            vec = vec0.copy()
            vec[0] += c
            ref_d_vec = conv.DistributionVec(*vec)
            sum_d_vec = d_vec0 + c
            rsum_d_vec = d_vec0 + c
            isum_d_vec = copy.deepcopy(d_vec0)
            isum_d_vec += c

            for d_other in [sum_d_vec, rsum_d_vec, isum_d_vec]:
                assert ref_d_vec.compare(d_other, x)

    def test_mul_const(self):
        cs = [1328, -435.421]

        vec0 = np.array([4.45, 2483, 7.452], dtype=float)
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for c in cs:
            vec = vec0.copy()
            vec *= c
            ref_d_vec = conv.DistributionVec(*vec)
            mul_d_vec = c * d_vec0
            rmul_d_vec = d_vec0 * c
            imul_d_vec = copy.deepcopy(d_vec0)
            imul_d_vec *= c

            for d_other in [mul_d_vec, rmul_d_vec, imul_d_vec]:
                assert ref_d_vec.compare(d_other, x)

    def test_compare(self):
        d_vec0 = conv.DistributionVec(lambda x: 4.45, 2483, 7.452)
        d_vec1 = conv.DistributionVec(lambda x: 4.44, 2483, 7.452)
        d_vec2 = conv.DistributionVec(4.45, 2484, 21.322)
        d_vec3 = conv.DistributionVec(2.756, 1233, 21.322)

        for x in [0.2, 0.7]:
            assert d_vec0.compare(d_vec0, x)
            assert d_vec0.compare(copy.deepcopy(d_vec0), x)

            for d_other in [d_vec1, d_vec2, d_vec3]:
                assert not d_vec0.compare(d_other, x)

        # error
        with pytest.raises(ValueError):
            d_vec0.compare(1, 1)


@pytest.mark.quick_check
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
        i = InterpolatorDispatcher(xg, 1, False, False)
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
        i = InterpolatorDispatcher(xg, 1, False, False)
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
        i = InterpolatorDispatcher(xg, 1, True, False)
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


# @pytest.mark.quick_check
# @pytest.mark.skip
class Test_operations:
    def test_add_d_vec(self):
        vecs = [
            [1, 2, 3],
            [lambda x: x, lambda x: x, 3897],
        ]
        vec0 = np.array([None, lambda x: x, 3897])
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for vec in vecs:
            ref_d_vec = conv.DistributionVec(*(np.array(vec)))
            sum_ = d_vec0.__add__(ref_d_vec)
            sumi_ = d_vec0.__iadd__(ref_d_vec)
            sumr_ = d_vec0.__radd__(ref_d_vec)
            ref_sum = conv.DistributionVec(*vec) + d_vec0

            assert ref_sum.compare(sum_, x)
            assert ref_sum.compare(sumi_, x)
            assert ref_sum.compare(sumr_, x)

    def test_add_other(self):

        reg0 = [None, lambda x: x, 1]
        others = [
            3,
            lambda x: x,
        ]

        for r in reg0:
            vec0 = np.array([r, lambda x: x, 3897])
            d_vec0 = conv.DistributionVec(*vec0)

            for o in others:
                sum_ = d_vec0.__add__(o)
                if o == None:
                    assert sum_.regular == o
                if o == callable:
                    x = 0.5
                    assert sum_regular(x) == o(x)

    def test_mul_d_vec(self):
        factors = [
            1,
            1003,
            4,
        ]
        vec0 = np.array([None, lambda x: x, 3897])
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for f in factors:
            prod_ = d_vec0.__mul__(f)
            prodi_ = d_vec0.__imul__(f)
            prodr_ = d_vec0.__rmul__(f)

            ref_mult = conv.DistributionVec(*vec0) * f

            assert ref_mult.compare(prod_, x)
            assert ref_mult.compare(prodi_, x)
            assert ref_mult.compare(prodr_, x)
