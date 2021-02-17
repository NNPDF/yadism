# -*- coding: utf-8 -*-
"""
Test the interface provided for the user.
"""

import pytest
import numpy as np
from collections.abc import Iterable
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
    "ModEv": "EXA",
}

obs_dict = {
    "observables": {"F2light": []},
    "interpolation_xgrid": [0.001, 0.01, 0.1, 0.5, 1.0],
    "prDIS": "EM",
    "PolarizationDIS": 0.0,
    "ProjectileDIS": "electron",
    "interpolation_is_log": 1.0,
    "interpolation_polynomial_degree": 4,
}


class TestInit:
    def test_run_yadism(self):
        o1 = yadism.run_yadism(theory_dict, obs_dict)
        o2 = yadism.runner.Runner(theory_dict, obs_dict).get_result().get_raw()
        for k in o1:
            if k in o2:
                if isinstance(o1[k], Iterable):
                    o1[k] = list(o1[k])
                assert np.all(o1[k] == o2[k])
