import numpy as np
from scipy.special import spence
import pytest

from yadism.coefficient_functions import splitting_functions as sf


def test_li2():
    for z in np.linspace(0.0, 1.0, 50):
        assert pytest.approx(sf.nlo.ns.li2(z)) == spence(1 - z)
