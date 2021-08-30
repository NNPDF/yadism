import numpy as np
import pytest
from scipy.special import spence

from yadism.coefficient_functions import special
from yadism.coefficient_functions.special.nielsen import nielsen


def test_li2():
    for z in np.linspace(0.0, 1.0, 50):
        assert pytest.approx(special.li2(z)) == spence(1 - z)


def test_nielsen():
    np.testing.assert_allclose(nielsen(1, 1, 1), np.pi ** 2 / 6.0)
    np.testing.assert_allclose(nielsen(1, 1, 0), 0.0)
    np.testing.assert_allclose(
        nielsen(1, 1, 0.5), np.pi ** 2 / 12.0 - np.log(2) ** 2 / 2.0
    )

    # MMa: N[PolyLog[1,2,3/10],10]
    np.testing.assert_allclose(nielsen(1, 2, 0.3), 0.02819134108)
    # MMa: N[PolyLog[2,1,3/10],10]
    np.testing.assert_allclose(nielsen(2, 1, 0.3), 0.3124001779)

    # MMa: N[PolyLog[2,3,9/10],10]
    np.testing.assert_allclose(nielsen(2, 3, 0.9), 0.04688868860)
    # MMa: N[PolyLog[3,2,-11/10],10]
    np.testing.assert_allclose(nielsen(3, 2, -1.1), 0.05802161975)

    # MMa: N[PolyLog[1, 1, 2], 10]
    np.testing.assert_allclose(nielsen(1, 1, 2.0), 2.467401100 - 2.177586090j)
    # MMa: N[PolyLog[1, 1, 3], 10]
    np.testing.assert_allclose(nielsen(1, 1, 3.0), 2.320180423 - 3.451392295j)
