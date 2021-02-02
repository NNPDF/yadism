# -*- coding: utf-8 -*-
"""
Test the Input Defaults. 
"""
import pytest

import pathlib

import yaml 

from yadism.input import errors, defaults

repo_path = pathlib.Path(__file__).absolute().parents[1]


# @pytest.mark.skip
class TestDefaultManager:

    def test_menager(self):
        
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
            "ModEv": "EXA",
            "DynScVar": 0,
            "ScVarProc": 0, 
            "DampPowerFONLL": 0, 
            "EWCouplings": 0, 
            "SFNLOQED": 1,
            "SelectedCharge": 1,
        }

        with open(f'{repo_path}/../src/yadism/input/defaults.yaml') as f:
            rules = yaml.safe_load(f)

        rules = rules["simple-defaults"]
        for rule in rules:
            _def = defaults.DefaultManager(rule)
            
            try: 
                _def( theory_dict )
            except:
                pytest.raises(errors.DefaultError)
