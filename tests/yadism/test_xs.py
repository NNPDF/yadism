import collections

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from yadism import xs
from yadism.esf import exs


class TestCrossSection:
    def test_init(self, capsys):
        test_xs = xs.CrossSection(None, None)

        assert test_xs.obs_name is None
        assert test_xs.runner is None
        assert test_xs.exss == []

    @given(st.lists(st.none()))
    def test_len_elems(self, elems):
        filled_xs = xs.CrossSection(None, None)

        assert len(filled_xs) == 0

        filled_xs.exss = elems

        assert len(filled_xs) == len(elems)
        assert filled_xs.elements == elems

    @given(st.text())
    def test_repr(self, name):
        ObsName = collections.namedtuple("ObsName", ["name"])
        named_xs = xs.CrossSection(ObsName(name), None)

        assert named_xs.obs_name.name == name
        assert repr(named_xs) == name
        assert str(named_xs) == name

    @given(st.lists(st.none()))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_load(self, monkeypatch, kinematic_configs):
        EXS = collections.namedtuple(
            "ObsName", ["kinematics", "name", "configs", "get_esf"]
        )
        FakeRunner = collections.namedtuple("FakeRunner", ["configs"])
        monkeypatch.setattr(exs, "EvaluatedCrossSection", EXS)

        filled_xs = xs.CrossSection(None, FakeRunner("ciao"))
        assert len(filled_xs) == 0

        filled_xs.load(kinematic_configs)
        assert len(filled_xs) == len(kinematic_configs)

    @given(st.text())
    def test_get_sf(self, name):
        class FakeRunner:
            def get_sf(self, name):
                return self

            def get_esf(self, name, *args, **kwargs):
                return self

        runner = FakeRunner()
        esf_provider_xs = xs.CrossSection(name, runner)

        assert esf_provider_xs.get_esf(name, None) == runner

    @given(st.lists(st.none()))
    def test_result(self, elems):
        filled_xs = xs.CrossSection(None, None)

        assert len(filled_xs) == 0

        class EXS:
            def __init__(self, id):
                self.id = id

            def get_result(self):
                return self.id

        filled_xs.exss = [EXS(id=idx) for idx in enumerate(elems)]

        assert len(filled_xs) == len(elems)
        assert filled_xs.get_result() == [el.id for el in filled_xs.exss]
