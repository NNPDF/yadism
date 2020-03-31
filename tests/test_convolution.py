import numpy as np
import pytest

import yadism.structure_functions.convolution as conv


class TestDistributionVec:
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
