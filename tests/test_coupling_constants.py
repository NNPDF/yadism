# -*- coding: utf-8 -*-
import numpy as np
import pytest

import yadism.coupling_constants as coupl


class TestCouplingConstanst:
    def test_init(self):
        coupl_const = coupl.CouplingConstants({}, {})
        # TODO: try to initialize with more configs and test the output

    def test_vectorial(self):
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict()
        assert coupl.CouplingConstants(th_d, obs_d).vectorial_coupling(21) == 0

    def test_get_weight(self):
        th_d = dict(sin2theta_weak=1.0)

        # NC
        obs_d = dict(projectilePID=11, polarization=0.0, process="EM")
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "F3") == 0
        th_d = dict(sin2theta_weak=0.5, MZ2=100)
        obs_d = dict(
            projectilePID=11, polarization=0.0, process="NC", propagatorCorrection=0.5,
        )
        assert coupl.CouplingConstants(th_d, obs_d).get_weight(1, 0, "F3") == 0

        # CC
        th_d = dict(
            sin2theta_weak=0.5,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict(prDIS="CC")
        assert coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
            1, 0, "F2", cc_flavor="bottom"
        ) == coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
            1, 0, "FL", cc_flavor="bottom"
        )
        assert coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
            1, 0, "F2", cc_flavor="bottom"
        ) == coupl.CouplingConstants.from_dict(th_d, obs_d).get_weight(
            1, 0, "F3", cc_flavor="bottom"
        )

        # Unknown
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict(projectilePID=11, polarization=0.0, process="XX")
        with pytest.raises(ValueError, match="Unknown"):
            coupl.CouplingConstants(th_d, obs_d).get_weight(1, 90, "F2")

    def test_from_dict(self):
        sin2tw = 0.5
        MZ = 80
        th_d = dict(
            SIN2TW=sin2tw,
            MZ=MZ,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict()
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)

        assert coupl_const.theory_config["MZ2"] == MZ ** 2
        assert coupl_const.theory_config["MW2"] == MZ ** 2 / (1 - sin2tw)

        th_d["MW"] = MW = 2
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)
        assert coupl_const.theory_config["MW2"] == MW ** 2

        # Unknown projectile
        obs_d["ProjectileDIS"] = 0
        with pytest.raises(ValueError, match="Unknown projectile"):
            coupl.CouplingConstants.from_dict(th_d, obs_d)


class TestLeptonicHadronic:
    def test_cc(self):
        th_d = dict(
            sin2theta_weak=1.0,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        )
        obs_d = dict()
        coupl_const = coupl.CouplingConstants.from_dict(th_d, obs_d)

        kinds = ["F2", "FL", "F3"]

        for kind in kinds:
            assert coupl_const.leptonic_coupling("WW", kind) == 2

        f2_coupl = coupl_const.hadronic_coupling("WW", kind, 4, cc_flavor="charm")
        for kind in kinds:
            assert (
                coupl_const.hadronic_coupling("WW", kind, 4, cc_flavor="charm")
                == f2_coupl
            )

    def test_pure_em(self):
        th_d = dict(sin2theta_weak=1.0)

        for projPID in [-12, -11, 11, 12]:
            obs_d = dict(projectilePID=projPID, polarization=0.0)
            coupl_const = coupl.CouplingConstants(th_d, obs_d)

            for method in ["leptonic_coupling", "hadronic_coupling"]:
                coupl_f = coupl_const.__getattribute__(method)

                pid = []
                if "hadronic" in method:
                    pid.append(3)

                assert coupl_f("phph", "F3", *pid) == 0
                assert coupl_f("phph", "F2", *pid) == coupl_f("phph", "FL", *pid)

    def test_nc_interference(self):
        th_d = dict(sin2theta_weak=1.0)

        obs_d_e = dict(projectilePID=11, polarization=0.5)
        coupl_const_e = coupl.CouplingConstants(th_d, obs_d_e)
        obs_d_an = dict(projectilePID=-11, polarization=-0.5)
        coupl_const_an = coupl.CouplingConstants(th_d, obs_d_an)

        for method in ["leptonic_coupling", "hadronic_coupling"]:
            coupl_e_f = coupl_const_e.__getattribute__(method)
            coupl_an_f = coupl_const_an.__getattribute__(method)

            pid = []
            if "hadronic" in method:
                pid.append(2)

            assert coupl_e_f("phZ", "F3", *pid) == coupl_an_f("phZ", "F3", *pid)

            for projPID in [-12, -11, 11, 12]:
                obs_d = dict(projectilePID=projPID, polarization=0.0)
                coupl_const = coupl.CouplingConstants(th_d, obs_d)

                coupl_f = coupl_const.__getattribute__(method)

                assert coupl_f("phZ", "F2", *pid) == coupl_f("phZ", "FL", *pid)

    def test_pure_z(self):
        th_d = dict(sin2theta_weak=1.0)

        obs_d_e = dict(projectilePID=12, polarization=0.7)
        coupl_const_e = coupl.CouplingConstants(th_d, obs_d_e)
        obs_d_an = dict(projectilePID=-12, polarization=-0.7)
        coupl_const_an = coupl.CouplingConstants(th_d, obs_d_an)

        for method in ["leptonic_coupling", "hadronic_coupling"]:
            coupl_e_f = coupl_const_e.__getattribute__(method)
            coupl_an_f = coupl_const_an.__getattribute__(method)

            pid = []
            if "hadronic" in method:
                pid.append(1)

            assert coupl_e_f("ZZ", "F3", *pid) == coupl_an_f("ZZ", "F3", *pid)

            for projPID in [-12, -11, 11, 12]:
                obs_d = dict(projectilePID=projPID, polarization=0.0)
                coupl_const = coupl.CouplingConstants(th_d, obs_d)

                coupl_f = coupl_const.__getattribute__(method)

                for qct in [None, "V", "A"]:
                    extras = {}
                    if "hadronic" in method:
                        extras = dict(quark_coupling_type=qct)

                    assert coupl_f("ZZ", "F2", *pid, **extras) == coupl_f(
                        "ZZ", "FL", *pid, **extras
                    )

    def test_unknown(self):
        th_d = dict(sin2theta_weak=1.0)
        obs_d = dict(projectilePID=12, polarization=0.7)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        for method in ["leptonic_coupling", "hadronic_coupling"]:
            coupl_f = coupl_const.__getattribute__(method)

            pid = []
            if "hadronic" in method:
                pid.append(2)

            with pytest.raises(ValueError, match="Unknown"):
                coupl_f("XX", "F2", *pid)


class TestPropagator:
    def test_cc(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=100, MW2=80 ** 2)
        obs_d = dict(propagatorCorrection=0)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("WW", 0.0) == 0.0

    def test_pure_em(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=80, MW2=100 ** 2)
        obs_d = dict(propagatorCorrection=0)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("phph", 91.2) == 1.0

    def test_nc_interference(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=100, MW2=80 ** 2)
        obs_d = dict(propagatorCorrection=0)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor("phZ", 0.0) == 0.0

    def test_pure_z(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=80, MW2=100 ** 2)
        obs_d = dict(propagatorCorrection=0)
        coupl_const = coupl.CouplingConstants(th_d, obs_d)

        assert coupl_const.propagator_factor(
            "phZ", 91.2
        ) ** 2 == coupl_const.propagator_factor("ZZ", 91.2)

    def test_unknown(self):
        th_d = dict(sin2theta_weak=0.5, MZ2=91.1876)
        obs_d = dict(propagatorCorrection=0)
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
            ckm[2, 1, 0]
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
        assert ckm.masked("light").m.sum() == 2
        assert ckm.masked("charm").m.sum() == 2
        assert ckm.masked("bottom").m.sum() == 2
        assert ckm.masked("top").m.sum() == 3
        # Unknown flavor
        with pytest.raises(ValueError, match="Unknown flavor"):
            ckm.masked("ciao")

    def test_from_str(self):
        ra = np.random.rand(9)
        ra_s = " ".join([str(x) for x in ra])
        assert (coupl.CKM2Matrix(ra ** 2).m == coupl.CKM2Matrix.from_str(ra_s).m).all()
