import numpy as np
import pytest

import yadism.coefficient_functions.coupling_constants as coupl

from .test_nc_kernels import MockCouplingConstants


class MockCouplingEMConstants(MockCouplingConstants):
    def __init__(self):
        self.charges = {1: -1 / 3, 2: 2 / 3, 3: -1 / 3, 4: 2 / 3, 5: -1 / 3, 6: 2 / 3}


class TestCouplingConstanst:
    def test_vectorial(self):
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict()
        assert coupl.CouplingConstants(th_d, obs_d).vectorial_coupling(21) == 0

    def test_get_weight(self):
        th_d = dict(sin2theta_weak=1.0)

        # EM
        obs_d = dict(
            projectilePID=11,
            polarization=0.0,
            process="EM",
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "VA") == 0
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "AV") == 0
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "AA") == 0
        # in NC at Q2=0 this actually is formally equal to EM
        th_d = dict(sin2theta_weak=0.5, MZ2=100)
        obs_d = dict(
            projectilePID=11,
            polarization=0.0,
            process="NC",
            propagatorCorrection=0.5,
            nc_pos_charge=None,
        )
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 0, "VA") == 0
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 0, "AV") == 0
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 0, "AA") == 0

        # CC - needs from_dict to convert CKM
        th_d = dict(
            sin2theta_weak=0.5,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(
            prDIS="CC",
            PolarizationDIS=0.0,
            PropagatorCorrection=0,
            NCPositivityCharge=None,
        )
        assert (
            coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
                1, 0, None, cc_mask="b"
            )
            == 0
        )

        # Unknown
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict(
            projectilePID=11,
            polarization=0.0,
            process="XX",
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        with pytest.raises(ValueError, match="Unknown"):
            coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "VV")

    def test_pos(self):
        th_d = dict(sin2theta_weak=1.0)

        # EM
        obs_d = dict(
            projectilePID=11,
            polarization=0.0,
            process="EM",
            propagatorCorrection=0,
            nc_pos_charge="up",
        )
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90.0, "VV") == 0.0
        assert (
            coupl.CouplingConstants(th_d, obs_d).get_weight(2, 90.0, "VV") == 4.0 / 9.0
        )
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(3, 90.0, "VV") == 0.0

        # must have no effect in CC
        th_d = dict(
            sin2theta_weak=0.5,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(
            prDIS="CC",
            PolarizationDIS=0.0,
            PropagatorCorrection=0,
            NCPositivityCharge="up",
        )
        assert not np.isclose(
            coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
                1, 90.0, None, cc_mask="dus"
            ),
            0.0,
        )

    def test_from_dict(self):
        sin2tw = 0.5
        MZ = 80
        th_d = dict(
            SIN2TW=sin2tw,
            MZ=MZ,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(
            PolarizationDIS=0.0,
            prDIS="EM",
            PropagatorCorrection=0,
            NCPositivityCharge=None,
        )
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)

        assert coupl_const.theory_config["MZ2"] == MZ**2
        assert coupl_const.theory_config["MW2"] == MZ**2 / (1 - sin2tw)

        th_d["MW"] = MW = 2
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)
        assert coupl_const.theory_config["MW2"] == MW**2

        new_th_ckm = dict(
            SIN2TW=sin2tw,
            MZ=MZ,
            CKM=[
                0.97428,
                0.22530,
                0.003470,
                0.22520,
                0.97345,
                0.041000,
                0.00862,
                0.04030,
                0.999152,
            ],
        )
        new_coupl_const = coupl.CouplingConstants.from_dict(new_th_ckm, obs_d)
        assert coupl_const.theory_config["CKM"] == new_coupl_const.theory_config["CKM"]

        # Unknown projectile
        obs_d["ProjectileDIS"] = 0
        with pytest.raises(ValueError, match="Unknown projectile"):
            coupl.CouplingConstants.from_dict(th_d, obs_d)

    def test_partonic_coupling_fl11(self):
        th_d = dict(
            SIN2TW=0.5,
            MZ=80,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(
            projectilePID=11,
            PolarizationDIS=0.0,
            prDIS="EM",
            PropagatorCorrection=0,
            NCPositivityCharge=None,
        )
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)
        eq = np.array(list(MockCouplingEMConstants().charges.values()), dtype=float)
        for pid in range(1, 7):
            mean_e = np.mean(eq[:pid])

            # quark coupling type is the average * charge
            np.testing.assert_allclose(
                coupl_const.partonic_coupling_fl11("phph", pid, pid, "VV"),
                coupl_const.electric_charge[pid] * mean_e,
            )


class TestLeptonicHadronic:
    def test_cc(self):
        th_d = dict(
            sin2theta_weak=1.0,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(
            prDIS="EM",
            projectilePID=11,
            PolarizationDIS=0.0,
            PropagatorCorrection=0,
            NCPositivityCharge=None,
        )
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)

        assert coupl_const.leptonic_coupling("WW", None) == 2

    def test_pure_em(self):
        th_d = dict(sin2theta_weak=1.0)

        for projPID in [-12, -11, 11, 12]:
            obs_d = dict(
                prDIS="EM",
                projectilePID=projPID,
                polarization=0.0,
                propagatorCorrection=0,
                nc_pos_charge=None,
            )
            coupl_const = coupl.CouplingConstants(th_d, obs_d)

            assert coupl_const.leptonic_coupling("phph", "VA") == 0
            if abs(projPID) == 12:  # VV for neutrinos is still 0 in pure EM
                assert coupl_const.leptonic_coupling("phph", "VV") == 0
            else:
                assert coupl_const.leptonic_coupling("phph", "VV") != 0

            assert coupl_const.partonic_coupling("phph", 1, "VA") == 0
            assert coupl_const.partonic_coupling("phph", 1, "VV") != 0

    def test_nc_interference(self):
        th_d = dict(sin2theta_weak=1.0)

        obs_d_em = dict(
            process="EM",
            projectilePID=11,
            polarization=0.5,
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        coupl_const_em = coupl.CouplingConstants(th_d, obs_d_em)
        obs_d_ep = dict(
            process="EM",
            projectilePID=-11,
            polarization=-0.5,
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        coupl_const_ep = coupl.CouplingConstants(th_d, obs_d_ep)

        assert coupl_const_em.leptonic_coupling(
            "phZ", "VA"
        ) == coupl_const_ep.leptonic_coupling("phZ", "VA")
        assert coupl_const_em.partonic_coupling(
            "phZ", 1, "VA"
        ) == coupl_const_ep.partonic_coupling("phZ", 1, "VA")

    def test_pure_z(self):
        th_d = dict(sin2theta_weak=1.0)

        obs_d_nu = dict(
            process="EM",
            projectilePID=12,
            polarization=0.7,
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        coupl_const_nu = coupl.CouplingConstants(th_d, obs_d_nu)
        obs_d_nubar = dict(
            process="EM",
            projectilePID=-12,
            polarization=-0.7,
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        coupl_const_nubar = coupl.CouplingConstants(th_d, obs_d_nubar)

        assert coupl_const_nu.leptonic_coupling(
            "ZZ", "VA"
        ) == coupl_const_nubar.leptonic_coupling("ZZ", "VA")
        assert coupl_const_nu.partonic_coupling(
            "ZZ", 1, "VA"
        ) == coupl_const_nubar.partonic_coupling("ZZ", 1, "VA")

    def test_unknown(self):
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict(
            process="EM",
            projectilePID=12,
            polarization=0.7,
            propagatorCorrection=0,
            nc_pos_charge=None,
        )
        coupl_const = coupl.CouplingConstants(th_d, obs_d)
        with pytest.raises(ValueError, match="Unknown"):
            coupl_const.leptonic_coupling("XX", "VV")
        with pytest.raises(ValueError, match="Unknown"):
            coupl_const.partonic_coupling("XX", 1, "VV")


class TestPropagator:
    def test_cc(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=100, MW2=80**2)
        obs_d = dict(process="EM", propagatorCorrection=0, nc_pos_charge=None)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("WW", 0.0) == 0.0

    def test_pure_em(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=80, MW2=100**2)
        obs_d = dict(process="EM", propagatorCorrection=0, nc_pos_charge=None)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("phph", 91.2) == 1.0

    def test_nc_interference(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=100, MW2=80**2)
        obs_d = dict(process="EM", propagatorCorrection=0, nc_pos_charge=None)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("phZ", 0.0) == 0.0

    def test_pure_z(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=80, MW2=100**2)
        obs_d = dict(process="EM", propagatorCorrection=0, nc_pos_charge=None)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor(
            "phZ", 91.2
        ) ** 2 == coupl_const.propagator_factor("ZZ", 91.2)

    def test_unknown(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=91.1876)
        obs_d = dict(process="EM", propagatorCorrection=0, nc_pos_charge=None)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        with pytest.raises(ValueError, match="Unknown"):
            coupl_const.propagator_factor("XX", 10)


class TestCKM2Matrix:
    def test_init(self):
        coupl.CKM2Matrix(np.arange(9))
        # it is mandatory a 3x3 matrix (so deserves len=9 input)
        with pytest.raises(ValueError, match="reshape"):
            coupl.CKM2Matrix(np.arange(4))

    def test_getitem(self):
        ckm = coupl.CKM2Matrix(np.arange(9))
        # tuple = !tuple
        assert (ckm[2] == ckm[(2,)]).all()
        # rank = 2
        with pytest.raises(KeyError, match="3x3"):
            _ = ckm[2, 1, 0]
        # names available
        assert ckm[2, 1] == 0
        assert ckm["c", 1] == ckm[4, 1]
        assert ckm["t", "b"] == 8
        assert ckm[2, 1] == ckm[2][0] == ckm[:, 1][0]

    def test_call(self):
        ckm = coupl.CKM2Matrix(np.arange(9))
        assert (ckm[2] == ckm(2)).all()
        assert (ckm[:, 1] == ckm(1)).all()

    def test_masked(self):
        ckm = coupl.CKM2Matrix(np.ones(9))
        # number of active elements
        assert ckm.masked("dus").m.sum() == 2
        assert ckm.masked("c").m.sum() == 2
        assert ckm.masked("b").m.sum() == 2
        assert ckm.masked("t").m.sum() == 3

    def test_from_str(self):
        ra = (0.5 * np.random.rand(9) + 1.0) / 1.5
        ra_s = " ".join([str(x) for x in ra])
        np.testing.assert_allclose(
            coupl.CKM2Matrix(ra**2).m, coupl.CKM2Matrix.from_str(ra_s).m
        )
