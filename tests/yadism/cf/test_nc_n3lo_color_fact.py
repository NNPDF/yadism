import numpy as np
from yadism.coefficient_functions.light.n3lo.common import fl, fls, flg, nc_color_factor


class MockCouplingConstants:
    def __init__(self):
        self.charges = {pid: np.random.rand() for pid in range(1, 7)}

    def average_partonic_coupling(self, pid):
        return self.charges[pid]


class MockCouplingEMConstants(MockCouplingConstants):
    def __init__(self):
        self.charges = {1: 2 / 3, 2: -1 / 3, 3: -1 / 3, 4: 2 / 3, 5: -1 / 3, 6: 2 / 3}


def test_fl_factors_electromagnetic():
    eq = np.array(list(MockCouplingEMConstants().charges.values()), dtype=float)
    for nf in range(1, 7):
        mean_e = np.average(eq[:nf])
        mean_e2 = np.average(eq[:nf] ** 2)
        np.testing.assert_allclose(fl(eq[:nf]), 3 * mean_e)
        np.testing.assert_allclose(fls(eq[:nf]), mean_e**2 / mean_e2)
        np.testing.assert_allclose(flg(eq[:nf]), mean_e**2 / mean_e2)


def test_nc_color_factor():
    coupling = MockCouplingConstants()
    charges = np.array(list(coupling.charges.values()), dtype=float)
    for nf in range(1, 7):
        np.testing.assert_allclose(
            fl(charges[:nf]), nc_color_factor(coupling, nf, "ns", False)
        )
        np.testing.assert_allclose(
            flg(charges[:nf]), nc_color_factor(coupling, nf, "g", False)
        )
        np.testing.assert_allclose(
            fls(charges[:nf]), nc_color_factor(coupling, nf, "s", False)
        )

    for nf in reversed(range(2, 7)):
        charges[nf - 1] = 0
        np.testing.assert_allclose(
            fl(charges[:nf]), nc_color_factor(coupling, nf, "ns", True)
        )
        np.testing.assert_allclose(
            flg(charges[:nf]), nc_color_factor(coupling, nf, "g", True)
        )
        np.testing.assert_allclose(
            fls(charges[:nf]), nc_color_factor(coupling, nf, "s", True)
        )
        charges = charges[:nf]
