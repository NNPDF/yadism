import numpy as np
import pytest
from scipy.special import spence

from yadism.coefficient_functions import special


def test_li2():
    for z in np.linspace(0.0, 1.0, 50):
        assert pytest.approx(special.li2(z)) == spence(1 - z)