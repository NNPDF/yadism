# -*- coding: utf-8 -*-
'''
Test SF and EvaluatedStructureFunction
'''

import pytest

from yadism import observable_name
from yadism.sf import StructureFunction
from eko.interpolation import InterpolatorDispatcher
from yadism.esf.esf import EvaluatedStructureFunction as ESF
import numpy as np 


class MockRunner:
    _observable_instances = {}


class MockObj:
    pass


class MockDict:
    def __getitem__(self, key):
        if key == "interpolator":
            xg = np.linspace(0.2, 1.0, 5)  # 0.2, 0.4, 0.6, 0.8, 1.0
            a = InterpolatorDispatcher(xg, 1, False, False)
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
            a.nf = lambda x: 1
            b.nf = 1
            a.get_areas = lambda Q2: [b]
            return a
        if key == "TMC":
            return 0
        if key == "scheme":
            try: 
                return self.scheme
            except AttributeError:
                return "FFNS"
        if key == "coupling_constants":
            a = MockObj()
            a.get_weight = lambda q, q2, t: 1
            return a
        if key == "pto":
            return 1
        if key == "nf_ff":
            return 3


    def __setitem__(self, key, value):
        if key == "scheme":
            self.scheme = value

#    return None


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
             # test repr 
             assert repr(sf) == str(obs_name)
             # test mapping to self
             assert len(sf._StructureFunction__ESFcache) == 0
             obj = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
             #assert isinstance(obj, ESFmap[obs_name.flavor_family])
             # check creation
             assert len(sf._StructureFunction__ESFcache) == 1
             assert list(sf._StructureFunction__ESFcache.values())[0] == obj
             # check caching
             obj2 = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
             assert len(sf._StructureFunction__ESFcache) == 1

             # check values
             kins =  [{"x": 0.5, "Q2": 1}, {"x": 0.5, "Q2": 2}, {"x": 0.9, "Q2": 1000}]
             sf.load(kins)
             for res in sf.get_result():
                 assert res.values.all() == 0.0 

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


class TestEvaluatedStructureFunction:
    
    def test_init_repr(self):

        sf = StructureFunction(
            observable_name.ObservableName("F3light"),
            MockRunner(),
            eko_components=MockDict(),
            theory_params=MockDict(),
            obs_params=MockDict(),
        )

        kins = [ dict(x=0.3, Q2=-4), dict(x=-1.3, Q2=4.0),  dict(x=0.3, Q2=4), ]

        for k in kins:
            try:
                esf = ESF(sf, k)
                assert esf.x == k["x"]
                assert repr(esf) == "F3light(x=0.300000,Q2=4.000000)"
            except ValueError:
                continue

    def test_get_result(self):
        
        for scheme in ["FFNS", "ZM-VFNS", "FONLL-A"]:
            theory_params = MockDict()
            theory_params["scheme"] = scheme
            sf = StructureFunction(
                observable_name.ObservableName("FLlight"),
                MockRunner(),
                eko_components=MockDict(),
                theory_params=theory_params,
                obs_params=MockDict(),
            )
            k = dict(x=0.3, Q2=4)
            esf = ESF(sf, k)
            assert (esf.get_result()).values.all() == 0.0 


        

