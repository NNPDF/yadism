# -*- coding: utf-8 -*-
"""
Test the interface provided for the user.
"""

import pytest

import yadism
import yadism.runner as Runner

theory_dict = {
    "Q0": 1,
    "PTO": 0,
    "alphas": 0.118,
    "Qref": 91.2,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    "XIF": 1,
    "XIR": 1,
    "TMC": 0,
    "FNS": "FFNS",
    "NfFF": 3,
    "DAMP": 0,
    "MP": 0.938,
    "IC": 0,
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
    "MZ": 91.1876,
    "MW": 90.398,
    "GF": 1.1663787e-05,
    "SIN2TW": 0.23126,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
}

obs_dict = {
    "interpolation_xgrid": [0.001, 0.01, 0.1, 0.5, 1.0],
    "prDIS": "EM",
    "PolarizationDIS": 0.0,
    "projectile": "electron",
}


class TestInit:
    def test_run_yadism(self):
        assert (
            yadism.run_yadism(theory_dict, obs_dict)
            == yadism.runner.Runner(theory_dict, obs_dict).get_output()
        )
