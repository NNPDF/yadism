# -*- coding: utf-8 -*-
"""
Test SF and EvaluatedStructureFunction
"""

import numpy as np
import pytest
from eko import thresholds
from eko.interpolation import InterpolatorDispatcher, XGrid

from yadism import observable_name
from yadism.esf import scale_variations as sv
from yadism.esf.esf import EvaluatedStructureFunction as ESF
from yadism.sf import StructureFunction


class MockObj:
    pass


xg = XGrid(np.linspace(0.2, 1.0, 5), False)   # 0.2, 0.4, 0.6, 0.8, 1.0
interpolator = InterpolatorDispatcher(xg, 1, False)
coupling_constants = MockObj()
coupling_constants.obs_config = dict(process="EM")
coupling_constants.get_weight = lambda q, q2, t: 1
threshold = thresholds.ThresholdsAtlas([50.0, np.inf, np.inf])
sv_manager = sv.ScaleVariations(
    order=0, interpolator=interpolator, activate_ren=False, activate_fact=False
)


class MockRunner:
    _observable_instances = {}
    managers = dict(
        interpolator=interpolator,
        threshold=threshold,
        coupling_constants=coupling_constants,
        sv_manager=sv_manager,
    )
    theory_params = dict(
        pto=0, scheme="FFNS", target=dict(Z=1, A=1), TMC=0, nf_ff=4, FONLL_damping=False
    )


@pytest.mark.skip
class TestStructureFunction:
    def test_get_esf_same_name(self):
        # setup env
        r = MockRunner()

        # becarefull about what the esf instantiation need
        for name in ["FL_light", "F2_light"]:
            obs_name = observable_name.ObservableName(name)
            sf = StructureFunction(
                obs_name,
                r,
            )
            # test repr
            assert repr(sf) == str(obs_name)
            # test mapping to self
            assert len(sf.cache) == 0
            obj = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
            # assert isinstance(obj, ESFmap[obs_name.flavor_family])
            # check creation
            assert len(sf.cache) == 1
            assert list(sf.cache.values())[0] == obj
            # check caching
            _obj2 = sf.get_esf(obs_name, {"x": 0.5, "Q2": 1})
            assert len(sf.cache) == 1

            # check values
            kins = [{"x": 0.5, "Q2": 1}, {"x": 0.5, "Q2": 2}, {"x": 0.9, "Q2": 1000}]
            sf.load(kins)
            for res in sf.get_result():
                assert res.orders[(0, 0, 0, 0)][0].all() == 0.0

    def test_get_esf_outside_grid(self):
        r = MockRunner()

        name = observable_name.ObservableName("FL_light")

        sf = StructureFunction(
            name,
            r,
        )
        with pytest.raises(ValueError):
            sf.get_esf(name, {"x": 0.1, "Q2": 1})


@pytest.mark.skip
class TestEvaluatedStructureFunction:
    def test_init_repr(self):

        sf = StructureFunction(
            observable_name.ObservableName("F2_light"),
            MockRunner(),
        )

        kins = [
            dict(x=0.3, Q2=-4),
            dict(x=-1.3, Q2=4.0),
            dict(x=0.3, Q2=4),
        ]

        for k in kins:
            try:
                esf = ESF(sf, k)
                assert esf.x == k["x"]
                assert repr(esf) == "F2_light_EM(x=0.300000,Q2=4.000000)"
            except ValueError:
                continue

    def test_get_result(self):

        for scheme in ["FFNS", "ZM-VFNS", "FONLL-A"]:
            r = MockRunner()
            r.theory_params["scheme"] = scheme
            r.theory_params["target"] = {"Z": 1, "A": 1}
            r.theory_params["m2hq"] = [1, 2, 3]
            sf = StructureFunction(
                observable_name.ObservableName("FL_light"),
                r,
            )
            k = dict(x=0.3, Q2=4)
            esf = ESF(sf, k)
            assert (esf.get_result()).orders[(0, 0, 0, 0)][0].all() == 0.0
