"""
Old distribution vector tests
"""

import copy

import numpy as np
import pytest

from yadism.coefficient_functions import partonic_channel as pc


# @pytest.mark.quick_check
@pytest.mark.skip
class TestInit:
    def test_init_zero(self):
        d_vecs = [
            pc.DistributionVec(None),
            pc.DistributionVec(None, None),
            pc.DistributionVec(None, None, None),
            pc.DistributionVec([None, None]),
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
            d_vec = pc.DistributionVec(*vec)
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
            d_vec = pc.DistributionVec(*vec)
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
@pytest.mark.skip
class TestSpecial:
    def test_rsl_from_distr_coeffs(self):
        regular = [lambda x: x]
        delta = 1
        coeffs = [1, 2, 3]
        res_singular = 0
        res_local = 0
        z = 0.3
        assert regular == pc.rsl_from_distr_coeffs(regular, delta, *coeffs)[0]
        for coeff in coeffs:
            res_singular += coeff * 1 / (1 - z) * np.log(1 - z) ** (coeff - 1)
            res_local += coeff * np.log(1 - z) ** (coeff) / (coeff)

        assert res_singular == pc.rsl_from_distr_coeffs(regular, delta, *coeffs)[1](z)
        assert res_local + delta == conv.rsl_from_distr_coeffs(regular, delta, *coeffs)[
            2
        ](z)

    def test_iter_zero(self):
        vec = [lambda x: x, 1, None]
        d_vec = pc.DistributionVec(*vec)

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
            d_vec = pc.DistributionVec(*vec)
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
        d_vec0 = pc.DistributionVec(*vec0)

        x = 0.5
        for vec in vecs:
            ref_d_vec = pc.DistributionVec(*(np.array(vec) + vec0))
            sum_d_vec = pc.DistributionVec(*vec) + d_vec0

            assert ref_d_vec.compare(sum_d_vec, x)

    def test_add_func(self):
        fs = [lambda x: 18, lambda x: (1 - x)]

        vec0 = np.array([2837, 91283, 3897], dtype=float)
        d_vec0 = pc.DistributionVec(*vec0)

        x = 0.5
        for f in fs:
            vec = vec0.copy()
            vec[0] += f(x)
            ref_d_vec = pc.DistributionVec(*vec)
            sum_d_vec = d_vec0 + f(x)

            assert ref_d_vec.compare(sum_d_vec, x)

    def test_add_const(self):
        cs = [1328, -435.421]

        vec0 = np.array([4.45, 2483, 7.452], dtype=float)
        d_vec0 = pc.DistributionVec(*vec0)

        x = 0.5
        for c in cs:
            vec = vec0.copy()
            vec[0] += c
            ref_d_vec = pc.DistributionVec(*vec)
            sum_d_vec = d_vec0 + c
            rsum_d_vec = d_vec0 + c
            isum_d_vec = copy.deepcopy(d_vec0)
            isum_d_vec += c

            for d_other in [sum_d_vec, rsum_d_vec, isum_d_vec]:
                assert ref_d_vec.compare(d_other, x)

    def test_mul_const(self):
        cs = [1328, -435.421]

        vec0 = np.array([4.45, 2483, 7.452], dtype=float)
        d_vec0 = pc.DistributionVec(*vec0)

        x = 0.5
        for c in cs:
            vec = vec0.copy()
            vec *= c
            ref_d_vec = pc.DistributionVec(*vec)
            mul_d_vec = c * d_vec0
            rmul_d_vec = d_vec0 * c
            imul_d_vec = copy.deepcopy(d_vec0)
            imul_d_vec *= c

            for d_other in [mul_d_vec, rmul_d_vec, imul_d_vec]:
                assert ref_d_vec.compare(d_other, x)

    def test_compare(self):
        d_vec0 = pc.DistributionVec(lambda x: 4.45, 2483, 7.452)
        d_vec1 = pc.DistributionVec(lambda x: 4.44, 2483, 7.452)
        d_vec2 = pc.DistributionVec(4.45, 2484, 21.322)
        d_vec3 = pc.DistributionVec(2.756, 1233, 21.322)

        for x in [0.2, 0.7]:
            assert d_vec0.compare(d_vec0, x)
            assert d_vec0.compare(copy.deepcopy(d_vec0), x)

            for d_other in [d_vec1, d_vec2, d_vec3]:
                assert not d_vec0.compare(d_other, x)

        # error
        with pytest.raises(ValueError):
            d_vec0.compare(1, 1)
