import numpy as np
import pytest

import yadism.structure_functions.convolution as conv


def against_known_grid(xs, f, coeff, res):
    for x, y in zip(xs, res):
        assert (
            pytest.approx(y, 1 / 1000.0)
            == conv.convnd(x, conv.DistributionVec(*coeff), f)[0]
        )


def against_known(x, f, coeff, res):
    assert (
        pytest.approx(res(x), 1 / 1000.0)
        == conv.convnd(x, conv.DistributionVec(*coeff), f)[0]
    )


def test_regular():
    # format: 3-lists
    # - f: pdf function
    # - kmat: transformation matrix element
    # - res: results from Mathematica
    known_tests = [[lambda x: x, lambda x: 1, lambda y: 1 - y]]

    xs = [0.2, 0.4, 0.6, 0.8]

    for test in known_tests:
        test[1] = [test[1]]
        for x in xs:
            against_known(x, *test)


def test_delta():
    # format: 3-lists
    # - f: pdf function
    # - kmat: transformation matrix element
    # - res: results from Mathematica
    known_tests = [[lambda x: x, lambda x: 1, lambda y: y]]

    xs = [0.2, 0.4, 0.6, 0.8]

    for test in known_tests:
        test[1] = [lambda x: 0, test[1]]
        for x in xs:
            against_known(x, *test)


def test_pd():
    # format: 3-lists
    # - f: pdf function
    # - kmat: transformation matrix element
    # - res: results from Mathematica
    known_tests = [[lambda x: 1, lambda x: 1, lambda y: np.log((1 - y) / y)]]

    xs = [0.2, 0.4, 0.6, 0.8]

    for test in known_tests:
        test[1] = [lambda x: 0, lambda x: 0, test[1]]
        for x in xs:
            against_known(x, *test)


def test_log_pd():
    # format: 3-lists
    # - f: pdf function
    # - kmat: transformation matrix element
    # - res: results from Mathematica
    known_tests = [
        [lambda x: 1, lambda x: 1, np.array([-1.40903, -1.06518, -0.497553, 0.725006])]
    ]

    xs = [0.2, 0.4, 0.6, 0.8]

    for test in known_tests:
        test[1] = [lambda x: 0, lambda x: 0, lambda x: 0, test[1]]
        against_known_grid(xs, *test)


def test_symmetric_conv():
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
        results.append(conv.convnd(x, kma, f)[0])

    assert pytest.approx(results[0], 1 / 1000.0) == results[1]
