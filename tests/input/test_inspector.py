# -*- coding: utf-8 -*-
"""
Test the Input Inspector. 
"""
import copy

import pytest

from yadism.input import inspector, errors


# @pytest.mark.skip
class TestInspector:
    def test_domain(self):
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

        obs_dict = dict(
            interpolation_xgrid=[0.001, 0.01, 0.1, 0.5, 1.0],
            prDIS="EM",
            PolarizationDIS=0.0,
            ProjectileDIS="electron",
            interpolation_is_log=1.0,
            interpolation_polynomial_degree=4,
            TargetDIS="proton",
            polDIS=0.1,
            DeltaR=0.9,
        )

        insp = inspector.Inspector(theory_dict, obs_dict)
        insp.check_domains()

        runcard = copy.deepcopy(theory_dict)
        runcard["FNS"] = "FNS"
        with pytest.raises(errors.DomainError, match="FNS"):
            insp = inspector.Inspector(runcard, obs_dict)
            insp.check_domains()

        runcard = copy.deepcopy(theory_dict)
        runcard["NfFF"] = 2
        with pytest.raises(errors.DomainError, match="NfFF"):
            insp = inspector.Inspector(runcard, obs_dict)
            insp.check_domains()

        runcard = copy.deepcopy(obs_dict)
        runcard["prDIS"] = "GR"
        with pytest.raises(errors.DomainError, match="prDIS"):
            insp = inspector.Inspector(theory_dict, runcard)
            insp.check_domains()

    #        runcard = copy.deepcopy(obs_dict)
    #        with pytest.raises(errors.DomainError, match="polDIS"):
    #        runcard["polDIS"] = -2
    #            insp = inspector.Inspector(theory_dict,runcard)
    #            insp.check_domains()

    @pytest.mark.skip
    def test_default(self):
        runcard = {}
        with pytest.raises(errors.DefaultError):
            insp = inspector.Inspector(runcard, runcard)
            insp.apply_default()

        insp = inspector.Inspector(runcard, runcard)
        insp.apply_default(missing_yields_error=False)
