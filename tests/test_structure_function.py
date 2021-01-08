# -*- coding: utf-8 -*-
import pytest

from yadism import observable_name
from yadism.sf import StructureFunction
from yadism.esf import esf


class MockRunner:
    _observable_instances = {}


class MockObj:
    pass


class MockDict:
    def __getitem__(self, key):
        if key == "interpolator":
            a = MockObj()
            a.xgrid = [0.2, 0.6, 1.0]
            a.xgrid_raw = [0.2, 0.6, 1.0]
            return a
        if key == "alpha_s":
            a = MockObj()
            a.a_s = lambda q2: 1
            return a
        if key in ["xiR", "xiF"]:
            return 1
        if key == "threshold":
            a = MockObj()
            b = MockObj()
            b.nf = 1
            a.get_areas = lambda Q2: [b]
            return a
        if key == "TMC":
            return 0
        return None


@pytest.mark.quick_check
class TestStructureFunction:
    def test_get_esf_same_name(self):
        # setup env
        r = MockRunner()
        eko_components = MockDict()
        theory_params = MockDict()
        obs_params = MockDict()

        # becarefull about what the esf instantiation need
        for name in ["FLlight", "F2light"]:
            obs_name = observable_name.ObservableName(name)
            sf = StructureFunction(
                obs_name,
                r,
                eko_components=eko_components,
                theory_params=theory_params,
                obs_params=obs_params,
            )
            # test mapping to self
            assert len(sf._StructureFunction__ESFcache) == 0
            obj = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
#            assert isinstance(obj, ESFmap[obs_name.flavor_family])
            # check creation
            assert len(sf._StructureFunction__ESFcache) == 1
            assert list(sf._StructureFunction__ESFcache.values())[0] == obj
            # check caching
            obj2 = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
            assert len(sf._StructureFunction__ESFcache) == 1

    def test_get_esf_outside_grid(self):
        r = MockRunner()
        eko_components = MockDict()
        theory_params = MockDict()
        obs_params = MockDict()

        name = observable_name.ObservableName("FLlight")

        sf = StructureFunction(
            name,
            r,
            eko_components=eko_components,
            theory_params=theory_params,
            obs_params=obs_params,
        )
        with pytest.raises(ValueError):
            sf.get_esf(name, {"x": 0.1, "Q2": 1})
