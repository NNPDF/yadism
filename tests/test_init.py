# -*- coding: utf-8 -*-
"""
Test the interface provided for the user.
"""

import pytest

import yadism
import yadism.runner as Runner

theory_dict = {
    "FNS": "FFNS",
    "Q0": 1,
    "NfFF": 3,
    "alphas": 0.118,
    "Qref": 91.2,
    "PTO": 0,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    "XIF": 1,
    "DAMP": 0,
    "XIR": 1,
    "TMC": 0,
    "MP": 0.938,
    "mc": 2,
    "mb": 4,
    "mt": 173.07,
}

obs_dict = {"interpolation_xgrid": [0.001, 0.01, 0.1, 0.5, 1.0]}


class TestInit:
    def test_run_yadism(self):
        assert (
            yadism.run_yadism(theory_dict, obs_dict)
            == yadism.runner.Runner(theory_dict, obs_dict).get_output()
        )
