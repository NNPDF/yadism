# -*- coding: utf-8 -*-
"""
Test the Input Inspector. 
"""
import copy

import pytest

from yadism.input import inspector, errors


@pytest.mark.skip
class TestInspector:
    def test_domain(self):
        passing_runcard = dict(
            FNS="FFNS",
            NfFF=3,
            prDIS="EM",
            ProjectileDIS="electron",
            TargetDIS="proton",
            polDIS=0.1,
            DeltaR=0.9,
        )

        insp = inspector.Inspector(passing_runcard)
        insp.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["FNS"] = "FNS"
        with pytest.raises(errors.DomainError, match="FNS"):
            insp = inspector.Inspector(runcard)
            insp.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["NfFF"] = 2
        with pytest.raises(errors.DomainError, match="NfFF"):
            insp = inspector.Inspector(runcard)
            insp.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["prDIS"] = "GR"
        with pytest.raises(errors.DomainError, match="prDIS"):
            insp = inspector.Inspector(runcard)
            insp.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["polDIS"] = -2
        with pytest.raises(errors.DomainError, match="polDIS"):
            insp = inspector.Inspector(runcard)
            insp.check_domains()

    def test_default(self):
        runcard = {}
        with pytest.raises(errors.DefaultError):
            insp = inspector.Inspector(runcard)
            insp.apply_default()

        insp = inspector.Inspector(runcard)
        insp.apply_default(missing_yields_error=False)
