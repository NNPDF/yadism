# -*- coding: utf-8 -*-
import collections
import contextlib
import dataclasses

import pytest
import rich.progress
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import yadism.input.compatibility
import yadism.input.inspector
from yadism import log, runner, sf


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
    @given(st.data())
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_init(self, monkeypatch, data):
        @dataclasses.dataclass
        class FakeInspector:
            theory: dict
            observables: dict

            def perform_all_checks(self):
                pass

        def fake_update(*args):
            return args

        monkeypatch.setattr(yadism.input.inspector, "Inspector", FakeInspector)
        monkeypatch.setattr(yadism.input.compatibility, "update", fake_update)

        pto = data.draw(st.integers(0, 2))
        masses = {f"m{q}": v + 2.0 for v, q in enumerate("cbt")}
        kthr = {f"kDIS{q}Thr": v + 2.0 for v, q in enumerate("cbt")}
        zm_masses = {f"ZM{q}": True for q in "cbt"}
        theory = dict(
            PTO=pto,
            PTODIS=pto,
            FNS="ZM-VFNS",
            NfFF=3,
            nf0=3,
            **masses,
            **kthr,
            **zm_masses,
            MaxNfPdf=6,
            MP=1.0,
            Q0=2.0,
            HQ="POLE",
            DAMP=1,
            IC=1,
            TMC=0,
            RenScaleVar=True,
            FactScaleVar=False,
            CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
            MW=100.0,
            MZ=100.0,
            GF=1.0,
        )
        xgrid = (
            [1e-5]
            + data.draw(
                st.lists(
                    st.floats(1e-4, 1.0 - 1e-4), min_size=1, max_size=10, unique=True
                )
            )
            + [1.0]
        )
        observables = dict(
            interpolation_xgrid=xgrid,
            interpolation_polynomial_degree=len(xgrid) - 2,
            interpolation_is_log=True,
            prDIS="CC",
            TargetDIS=dict(Z=1.0, A=2.0),
            ProjectileDIS="electron",
            PolarizationDIS=0.0,
            PropagatorCorrection=0.0,
            observables={
                "F2_charm": [dict(x=0.1, Q2=10.0)],
                "XSCHORUSCC": [dict(x=0.1, y=0.5, Q2=10.0)],
            },
        )

        full_runner = runner.Runner(theory, observables)

        assert full_runner._theory["PTO"] == theory["PTO"]

        log.silent_mode = True
        theory["DAMP"] = 0

        full_runner = runner.Runner(theory, observables)

        assert full_runner.console.file is not None

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
        @dataclasses.dataclass
        class FakeESF:
            Q2: float

            def get_result(self):
                return None

        class FakeSF:
            def __init__(self, name):
                self.name = name
                self.elements = [FakeESF(Q2) for Q2 in range(1, 4)]

            def __len__(self):
                return len(self.elements)

        obss = {name: FakeSF(name) for name in names}
        results_runner = ResultsRunner(obss)

        @contextlib.contextmanager
        def fake_progress(*args, **kwargs):
            class FakeProgress:
                def add_task(self, *args, **kwargs):
                    return None

                def update(self, *args, **kwargs):
                    pass

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
