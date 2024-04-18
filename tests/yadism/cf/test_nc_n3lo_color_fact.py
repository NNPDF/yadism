# import numpy as np
# import pytest

# import yadism.coefficient_functions.coupling_constants as coupl
# from yadism.coefficient_functions.light.n3lo.common import fl, flg, fls, nc_color_factor


# class MockCouplingConstants:
#     def __init__(self):
#         self.charges = {pid: np.random.rand() for pid in range(1, 7)}

#     def linear_partonic_coupling(self, pid):
#         return self.charges[pid]


# class MockCouplingEMConstants(MockCouplingConstants):
#     def __init__(self):
#         self.charges = {1: 2 / 3, 2: -1 / 3, 3: -1 / 3, 4: 2 / 3, 5: -1 / 3, 6: 2 / 3}


# def test_fl_factors_electromagnetic():
#     eq = np.array(list(MockCouplingEMConstants().charges.values()), dtype=float)
#     for nf in range(1, 7):
#         mean_e = np.average(eq[:nf])
#         mean_e2 = np.average(eq[:nf] ** 2)
#         np.testing.assert_allclose(fl(eq[:nf]), 3 * mean_e)
#         np.testing.assert_allclose(fls(eq[:nf]), mean_e**2 / mean_e2)
#         np.testing.assert_allclose(flg(eq[:nf]), mean_e**2 / mean_e2)


# def test_fl_factors_cc():
#     th_d = dict(
#         SIN2TW=0.5,
#         MZ=80,
#         CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
#     )
#     obs_d = dict(
#         PolarizationDIS=0.0,
#         prDIS="CC",
#         PropagatorCorrection=0,
#         NCPositivityCharge=None,
#     )
#     coupl_cc = coupl.CouplingConstants.from_dict(th_d, obs_d)
#     for nf in range(1, 7):
#         np.testing.assert_allclose(nc_color_factor(coupl_cc, nf, "ns", False), 0.0)
#         np.testing.assert_allclose(nc_color_factor(coupl_cc, nf, "s", False), 0.0)
#         np.testing.assert_allclose(nc_color_factor(coupl_cc, nf, "g", False), 0.0)


# def test_nc_color_factor():
#     coupling = MockCouplingConstants()
#     charges = np.array(list(coupling.charges.values()), dtype=float)
#     for nf in range(1, 7):
#         np.testing.assert_allclose(
#             fl(charges[:nf]), nc_color_factor(coupling, nf, "ns", False)
#         )
#         np.testing.assert_allclose(
#             flg(charges[:nf]), nc_color_factor(coupling, nf, "g", False)
#         )
#         np.testing.assert_allclose(
#             fls(charges[:nf]) - fl(charges[:nf]),
#             nc_color_factor(coupling, nf, "s", False),
#         )

#     for nf in reversed(range(2, 7)):
#         charges[nf - 1] = 0
#         np.testing.assert_allclose(
#             fl(charges[:nf]), nc_color_factor(coupling, nf, "ns", True)
#         )
#         np.testing.assert_allclose(
#             flg(charges[:nf]), nc_color_factor(coupling, nf, "g", True)
#         )
#         np.testing.assert_allclose(
#             fls(charges[:nf]) - fl(charges[:nf]),
#             nc_color_factor(coupling, nf, "s", True),
#         )
#         charges = charges[:nf]

#     with pytest.raises(ValueError):
#         nc_color_factor(coupling, nf, "blabla", False)
