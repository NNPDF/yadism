# -*- coding: utf-8 -*-
import pytest

from yadism.input import constraints


class TestArgument:
    def test_string_argument(self):
        dom_def = dict(
            name="ciao",
            known_as="come",
            runcard="theory",
            description="va?",
            type="string",
        )
        checker = constraints.StringArgument(**dom_def)
        checker.check_value(value="bene")

        with pytest.raises(constraints.errors.DomainError, match="3"):
            checker.check_value(value=3)

    def test_enum_argument(self):
        dom_def = dict(
            name="ciao",
            known_as="come",
            runcard="theory",
            description="va?",
            type="enum",
            domain=["bene", "male", 3],
        )
        checker = constraints.EnumArgument(**dom_def)
        checker.check_value(value="bene")
        checker.check_value(value=3)

        with pytest.raises(constraints.errors.DomainError, match="cosicosi"):
            checker.check_value(value="cosicosi")

    def test_real_argument(self):
        dom_def = dict(
            name="ciao",
            known_as="come",
            runcard="theory",
            description="va?",
            type="real",
            domain=["0 < come < 4"],  # connected interval
        )
        checker = constraints.RealArgument(**dom_def)
        checker.check_value(value=3)

        with pytest.raises(constraints.errors.DomainError, match="10000"):
            checker.check_value(value=1e4)

        # disjoint intervals
        dom_def["domain"] = ["come > 0", "come < -4"]
        checker = constraints.RealArgument(**dom_def)
        checker.check_value(value=-5)
        with pytest.raises(constraints.errors.DomainError, match="-3"):
            checker.check_value(value=-3)

    def test_integer_argument(self):
        dom_def = dict(
            name="ciao",
            known_as="come",
            runcard="theory",
            description="va?",
            type="integer",
            domain=["0 < come < 4"],
        )
        checker = constraints.IntegerArgument(**dom_def)
        checker.check_value(value=3)

        with pytest.raises(constraints.errors.DomainError, match="3.01"):
            checker.check_value(value=3.01)

        with pytest.raises(constraints.errors.DomainError, match="5"):
            checker.check_value(value=5)


class TestCrossConstraint:
    pass
