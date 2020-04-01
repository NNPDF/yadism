import numpy as np
import pytest

import yadism.structure_functions.convolution as conv


class TestInit:
    def test_init_zero(self):
        d_vecs = [
            conv.DistributionVec(0),
            conv.DistributionVec(lambda x: 0),
            conv.DistributionVec(None),
            conv.DistributionVec(None, None),
            conv.DistributionVec(None, None, None),
            conv.DistributionVec(None, None, None, None),
            conv.DistributionVec([None, None]),
        ]

        for d_vec in d_vecs:
            for x in [0.1, 0.3, 0.5, 0.9]:
                assert d_vec[0](x) == 0
                assert d_vec[1](x) == 0
                assert d_vec[2](x) == 0
                assert d_vec[3](x) == 0
            # for c in d_vec:
            # assert c[0](x) == 0

    def test_init_const(self):
        vecs = [
            [1, 1, 1, 1],
            [1.0, 1.0, 1.0, 1.0],
            [lambda x: 1, lambda x: 1, 1, lambda x: 1],
            [1, 1, lambda x: 1, 1],
            [[1, 1, 1, 1,]],
            [[1, 1, 1, lambda x: 1]],
            [[lambda x: 1, 1, 1, 1]],
        ]

        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            for i in range(len(vec)):
                for x in [0.1, 0.3, 0.5, 0.9]:
                    assert d_vec[i](x) == 1
            # for c in d_vec:
            # assert c[0](x) == 0

    def test_init_different(self):
        """
        Keep this separate from the previous one because it
        is more involved, since we are not comparing with a 
        fixed target.
        """
        vecs = [
            [1, 2, 3, 4],
            [1, lambda x: 2, 103, 2004],
            [1, 202, 3],
            [1, None, 3, 504],
            [[1, 2, 3, 4]],
            [[1, 2, 703, lambda x: 4]],
            [[lambda x: 1, 492, 3, 4]],
        ]

        x = 0.5
        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            if isinstance(vec[0], list):
                vec = vec[0]

            for i in range(len(vec)):
                vtmp = vec[i]
                if callable(vtmp):
                    vi = vtmp(x)
                elif vtmp is None:
                    vi = 0
                else:
                    vi = float(vtmp)

                assert d_vec[i](x) == vi


class TestSpecial:
    def test_iter(self):
        vecs = [
            [1, 2, 3, 4],
            [1001, 2, 103, 2004],
        ]

        x = 0.5
        for vec in vecs:
            d_vec = conv.DistributionVec(*vec)
            if isinstance(vec[0], list):
                vec = vec[0]

            for i, c in enumerate(d_vec):
                assert vec[i] == c(x)

    def test_add_d_vec(self):
        vecs = [
            [1, 2, 3, 4],
            [1001, 2, 103, 2004],
        ]
        vec0 = np.array([2837, 91283, 3897, 293])
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for vec in vecs:
            ref_d_vec = conv.DistributionVec(*(np.array(vec) + vec0))
            sum_d_vec = conv.DistributionVec(*vec) + d_vec0

            for ref_c, sum_c in zip(ref_d_vec, sum_d_vec):
                assert ref_c(x) == sum_c(x)

    def test_add_func(self):
        fs = [lambda x: 18, lambda x: (1 - x)]

        vec0 = np.array([2837, 91283, 3897, 293], dtype=float)
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for f in fs:
            vec = vec0.copy()
            vec[0] += f(x)
            ref_d_vec = conv.DistributionVec(*vec)
            sum_d_vec = f + d_vec0

            for ref_c, sum_c in zip(ref_d_vec, sum_d_vec):
                assert ref_c(x) == sum_c(x)

    def test_add_const(self):
        cs = [1328, -435.421]

        vec0 = np.array([4.45, 2483, 7.452, 293.03], dtype=float)
        d_vec0 = conv.DistributionVec(*vec0)

        x = 0.5
        for c in cs:
            vec = vec0.copy()
            vec[0] += c
            ref_d_vec = conv.DistributionVec(*vec)
            sum_d_vec = c + d_vec0

            for ref_c, sum_c in zip(ref_d_vec, sum_d_vec):
                assert ref_c(x) == sum_c(x)


# @pytest.mark.skip
class TestConvnd:
    @staticmethod
    def against_known_grid(xs, f, coeff, res):
        for x, y in zip(xs, res):
            assert (
                pytest.approx(y, 1 / 1000.0)
                == conv.DistributionVec(coeff).convnd(x, f)[0]
            )

    @staticmethod
    def against_known(x, f, coeff, res):
        assert (
            pytest.approx(res(x), 1 / 1000.0)
            == conv.DistributionVec(*coeff).convnd(x, f)[0]
        )

    def test_regular(self):
        # format: 3-lists
        # - f: pdf function
        # - kmat: transformation matrix element
        # - res: results from Mathematica
        known_tests = [[lambda x: x, lambda x: 1, lambda y: 1 - y]]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            test[1] = [test[1]]
            for x in xs:
                self.against_known(x, *test)

    def test_delta(self):
        # format: 3-lists
        # - f: pdf function
        # - kmat: transformation matrix element
        # - res: results from Mathematica
        known_tests = [[lambda x: x, lambda x: 1, lambda y: y]]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            test[1] = [lambda x: 0, test[1]]
            for x in xs:
                self.against_known(x, *test)

    def test_pd(self):
        # format: 3-lists
        # - f: pdf function
        # - kmat: transformation matrix element
        # - res: results from Mathematica
        known_tests = [[lambda x: 1, lambda x: 1, lambda y: np.log((1 - y) / y)]]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            test[1] = [lambda x: 0, lambda x: 0, test[1]]
            for x in xs:
                self.against_known(x, *test)

    def test_log_pd(self):
        # format: 3-lists
        # - f: pdf function
        # - kmat: transformation matrix element
        # - res: results from Mathematica
        known_tests = [
            [
                lambda x: 1,
                lambda x: 1,
                np.array([-1.40903, -1.06518, -0.497553, 0.725006]),
            ]
        ]

        xs = [0.2, 0.4, 0.6, 0.8]

        for test in known_tests:
            test[1] = [lambda x: 0, lambda x: 0, lambda x: 0, test[1]]
            self.against_known_grid(xs, *test)

    def test_symmetric_conv(self):
        x = 0.4
        xg = np.arange(0.0, 1.0, 0.0001)
        xx = xg[np.searchsorted(xg, x)]

        kmas = [
            [lambda x: 1, lambda x: 0, lambda x: 0, lambda x: 0],
            [lambda x: x, lambda x: 0, lambda x: 0, lambda x: 0],
        ]
        fs = [lambda x: x, lambda x: 1]

        results = []
        for f, kma in zip(fs, kmas):
            results.append(conv.DistributionVec(kma).convnd(x, f)[0])

        assert pytest.approx(results[0], 1 / 1000.0) == results[1]
