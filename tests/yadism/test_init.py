"""Test the interface provided for the user."""

import numpy as np

import yadism

theory_dict = {
    "Q0": 1,
    "nf0": 3,
    "PTO": 0,
    "alphas": 0.118,
    "Qref": 91.2,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    "XIF": 1,
    "XIR": 1,
    "TMC": 0,
    "FNS": "FFNS",
    "NfFF": 5,
    "DAMP": 0,
    "MP": 0.938,
    "HQ": "POLE",
    "mc": 2,
    "mb": 4,
    "mt": 173.07,
    "Qmc": 2,
    "Qmb": 4,
    "Qmt": 173.07,
    "kcThr": 1.0,
    "kbThr": 1.0,
    "ktThr": 1.0,
    "MaxNfPdf": 6,
    "MaxNfAs": 6,
    "MZ": 91.1876,
    "MW": 90.398,
    "GF": 1.1663787e-05,
    "SIN2TW": 0.23126,
    "ModEv": "EXA",
    "n3lo_cf_variation": 0,
}

obs_dict = {
    "observables": {"": []},
    "interpolation_xgrid": [0.001, 0.01, 0.1, 0.5, 1.0],
    "prDIS": "EM",
    "PolarizationDIS": 0.0,
    "ProjectileDIS": "electron",
    "TargetDIS": "proton",
    "PropagatorCorrection": 0.0,
    "interpolation_is_log": 1.0,
    "interpolation_polynomial_degree": 4,
    "NCPositivityCharge": None,
}


class TestInit:

    kin_point = {"Q2": 2.0, "x": 0.1, "y": 0.1}

    def test_run_yadism(self):
        for obs in ["XSHERACC_charm", "XSHERACC_light"]:
            for current in ["EM", "NC", "CC"]:
                obs_dict["prDIS"] = current
                obs_dict["observables"] = {obs: [self.kin_point]}
                o1 = yadism.run_yadism(theory_dict, obs_dict)
                o1 = o1[obs][0].get_raw()
                o2 = yadism.runner.Runner(theory_dict, obs_dict).get_result().get_raw()
                for k in o1:
                    if k in o2:
                        assert np.all(o1[k] == o2[k])
