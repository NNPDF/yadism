# -*- coding: utf-8 -*-
"""
Test the Input Inspector. 
"""
import copy

import pytest

import yadism.input as input_


class TestErrors:
    def test_domain_error(self):
        with pytest.raises(input_.errors.DomainError):
            raise input_.errors.DomainError(
                name="test",
                description="test_description",
                type=type(3),
                known_as="ciao",
                value=3,
            )


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

        inspector = input_.inspector.Inspector(passing_runcard)
        inspector.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["FNS"] = "FNS"
        with pytest.raises(input_.errors.DomainError, match="FNS"):
            inspector = input_.inspector.Inspector(runcard)
            inspector.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["NfFF"] = 2
        with pytest.raises(input_.errors.DomainError, match="NfFF"):
            inspector = input_.inspector.Inspector(runcard)
            inspector.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["prDIS"] = "GR"
        with pytest.raises(input_.errors.DomainError, match="prDIS"):
            inspector = input_.inspector.Inspector(runcard)
            inspector.check_domains()

        runcard = copy.deepcopy(passing_runcard)
        runcard["polDIS"] = -2
        with pytest.raises(input_.errors.DomainError, match="polDIS"):
            inspector = input_.inspector.Inspector(runcard)
            inspector.check_domains()

    def test_default(self):
        runcard = {}
        with pytest.raises(input_.errors.DefaultError):
            inspector = input_.inspector.Inspector(runcard)
            inspector.apply_default()

        inspector = input_.inspector.Inspector(runcard)
        inspector.apply_default(missing_yields_error=False)


if __name__ == "__main__":
    # import warnings

    # warnings.simplefilter("error")
    TestInspector().test_default()
