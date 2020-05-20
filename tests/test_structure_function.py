# -*- coding: utf-8 -*-
import pytest

# from eko.interpolation import InterpolatorDispatcher

from yadism.sf import StructureFunction
from yadism.structure_functions import ESFmap


class MockRunner:
    _observable_instances = {}


class MockObj:
    pass


class MockDict:
    def __getitem__(self, key):
        if key == "interpolator":
            a = MockObj()
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
    def test_get_ESF_same_name(self):
        # setup env
        r = MockRunner()
        eko_components = MockDict()
        theory_stuffs = MockDict()

        # becarefull about what the esf instantiation need
        for name in ["FLlight", "F2light"]:
            sf = StructureFunction(
                name, r, eko_components=eko_components, theory_stuffs=theory_stuffs
            )
            # test mapping to self
            assert sf._StructureFunction__ESF == ESFmap[name]
            assert len(sf._StructureFunction__ESFcache) == 0
            obj = sf.get_ESF(name, {"x": 0.5, "Q2": 1})
            assert isinstance(obj, ESFmap[name])
            # check creation
            assert len(sf._StructureFunction__ESFcache) == 1
            assert list(sf._StructureFunction__ESFcache.values())[0] == obj
            # check caching
            obj2 = sf.get_ESF(name, {"x": 0.5, "Q2": 1})
            assert len(sf._StructureFunction__ESFcache) == 1

    def test_get_ESF_outside_grid(self):
        r = MockRunner()
        eko_components = MockDict()
        theory_stuffs = MockDict()

        name = "FLlight"

        sf = StructureFunction(
            name, r, eko_components=eko_components, theory_stuffs=theory_stuffs
        )
        with pytest.raises(ValueError):
            sf.get_ESF(name, {"x": 0.1, "Q2": 1})
