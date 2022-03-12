# -*- coding: utf-8 -*-
import collections
import contextlib

import pytest
import rich.progress
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from yadism import runner, sf


class DropRunner(runner.Runner):
    def __init__(self):
        class DropSF(sf.StructureFunction):
            def __init__(self):
                self.passed = False

            def drop_cache(self):
                self.passed = True

        class DropXS:
            def __init__(self):
                self.passed = True

        self.observables = dict(a=DropSF(), b=DropXS(), c=DropSF(), d=DropXS())


class GetRunner(runner.Runner):
    def __init__(self):
        self.observables = dict(a=None)


class ResultsRunner(runner.Runner):
    def __init__(self, observables):
        self.observables = observables
        self._observables = dict(observables={obs: [] for obs in observables})
        self._output = {}

        class FakeConsole:
            def __init__(self):
                self.content = []

            def print(self, *args):
                self.content.extend(args)

        self.console = FakeConsole()


class TestRunner:
    def test_init(self):
        #  runner.Runner({}, {})
        pass

    @given(st.text(min_size=2))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_get_sf(self, monkeypatch, name):
        FakeName = collections.namedtuple("FakeName", ["name"])
        FakeSF = collections.namedtuple("FakeSF", ["obsname", "runner"])
        get_runner = GetRunner()

        assert get_runner.get_sf(FakeName("a")) is None
        monkeypatch.setattr(runner, "SF", FakeSF)
        assert get_runner.get_sf(FakeName(name)).obsname.name == name

    def test_drop(self):
        drop_runner = DropRunner()

        drop_runner.drop_cache()
        assert all(o.passed for o in drop_runner.observables.values())

    @given(st.lists(st.text()))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_result(self, monkeypatch, names):
        FakeSF = collections.namedtuple("FakeSF", ["name", "runner", "elements"])
        obss = {name: FakeSF(name, None, []) for name in names}
        results_runner = ResultsRunner(obss)

        @contextlib.contextmanager
        def fake_progress(*args, **kwargs):
            class FakeProgress:
                def add_task(self, *args, **kwargs):
                    return None

            yield FakeProgress()

        monkeypatch.setattr(rich.progress, "Progress", fake_progress)
        assert results_runner.get_result() is not None


class TestConfig:
    @given(st.text(), st.text())
    def test_init(self, theory, managers):
        config = runner.RunnerConfigs(theory, managers)

        assert config.theory == theory
        assert config.managers == managers

    @given(
        st.dictionaries(st.text(), st.floats()),
        st.dictionaries(st.text(), st.functions()),
        st.data(),
    )
    def test_getattribute(self, theory, managers, data):
        theory["mykey"] = None
        theory["anotherkey"] = data.draw(st.binary())
        managers["mykey"] = data.draw(st.integers())
        managers["yourkey"] = data.draw(st.characters())
        config = runner.RunnerConfigs(theory, managers)

        assert config.mykey == managers["mykey"]
        assert config.yourkey == managers["yourkey"]
        assert config.anotherkey == theory["anotherkey"]
        assert isinstance(config.theory, dict)

        managers["theory"] = data.draw(st.text())
        config = runner.RunnerConfigs(theory, managers)

        assert config.theory == managers["theory"]
        with pytest.raises(AttributeError):
            config.missing
