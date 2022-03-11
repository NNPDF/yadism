# -*- coding: utf-8 -*-
from hypothesis import given
from hypothesis import strategies as st

from yadism import runner


class TestRunner:
    def test_init(self):
        #  runner.Runner(theory=theory, observables=observables)
        pass


class TestConfig:
    @given(st.text(), st.text())
    def test_init(self, theory, managers):
        config = runner.RunnerConfigs(theory, managers)

        assert config.theory == theory
        assert config.managers == managers

    @given(
        st.dictionaries(st.text(), st.floats()),
        st.dictionaries(st.text(), st.functions()),
        st.integers(),
    )
    def test_getattribute(self, theory, managers, value):
        managers["mykey"] = value
        managers["yourkey"] = value
        theory["mykey"] = None
        config = runner.RunnerConfigs(theory, managers)

        assert config.mykey == value
        assert config.yourkey == value
        assert isinstance(config.theory, dict)

        managers["theory"] = value
        config = runner.RunnerConfigs(theory, managers)

        assert config.theory == value
