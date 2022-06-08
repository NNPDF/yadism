# -*- coding: utf-8 -*-
import pytest

from yadism.coefficient_functions import kernels


# @pytest.mark.quick_check
@pytest.mark.skip
class Test_operations:
    def test_add_d_vec(self):
        vecs = [
            [1, 2, 3],
            [lambda x: x, lambda x: x, 3897],
        ]
        vec0 = np.array([None, lambda x: x, 3897])
        d_vec0 = kernels.DistributionVec(*vec0)

        x = 0.5
        for vec in vecs:
            ref_d_vec = kernels.DistributionVec(*(np.array(vec)))
            sum_ = d_vec0.__add__(ref_d_vec)
            sumi_ = d_vec0.__iadd__(ref_d_vec)
            sumr_ = d_vec0.__radd__(ref_d_vec)
            ref_sum = kernels.DistributionVec(*vec) + d_vec0

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
            d_vec0 = kernels.DistributionVec(*vec0)

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
        d_vec0 = kernels.DistributionVec(*vec0)

        x = 0.5
        for f in factors:
            prod_ = d_vec0.__mul__(f)
            prodi_ = d_vec0.__imul__(f)
            prodr_ = d_vec0.__rmul__(f)

            ref_mult = kernels.DistributionVec(*vec0) * f

            assert ref_mult.compare(prod_, x)
            assert ref_mult.compare(prodi_, x)
            assert ref_mult.compare(prodr_, x)
