# -*- coding: utf-8 -*-
import pytest

import yadism.observable_name as on
from yadism.observable_name import ObservableName as ON


class TestObservableName:
    def test_init(self):
        with pytest.raises(ValueError):
            _ = ON("F2blub")
        with pytest.raises(ValueError):
            _ = ON("j2charm")

    def test_all(self):
        all_obs_names = [o.name for o in ON.all()]
        assert "F2light" in all_obs_names
        # [2,L,3] * [l,t,(c,b,t)*(-,asy,light)]
        assert len(all_obs_names) == 3 * (1 + 1 + 3 * 3)

    def test_f2light(self):
        k = "F2"
        f = "light"
        n = k + f
        o = ON(n)
        assert o.kind == k
        assert o.flavor == f
        assert o.raw_flavor == o.flavor
        assert o.name == n
        assert str(o) == n
        assert o.flavor_family == f
        assert o.mass_label is None

        assert not o.is_heavy
        assert not o.is_raw_heavy
        assert not o.is_asy
        assert not o.is_composed

        assert o != ON("FL" + f)
        assert o.apply_kind("FL").flavor == f
        assert o == o.apply_flavor_family()
        assert ON.is_valid(n)
        assert ON.has_lights(["abc", n])
        assert not ON.has_heavies(["abc", n])

        # check asy
        with pytest.raises(ValueError):
            o.apply_asy()

    def test_fxc(self):
        k = "F2"
        f = "charm"
        n = k + f
        o = ON(n)
        assert o.kind == k
        assert o.flavor == f
        assert o.name == n
        assert str(o) == n
        assert o.flavor_family == "heavy"
        assert o.mass_label == "mc"
        assert o.hqnumber == 4

        assert o.is_heavy
        assert o.is_raw_heavy
        assert not o.is_asy
        assert not o.is_composed

        assert o != ON("FL" + f)
        assert o.apply_kind("FL").flavor == f
        assert ON.is_valid(n)
        assert not ON.has_lights(["abc", n])
        assert ON.has_heavies(["abc", n])

        # check asy
        oa = o.apply_asy()
        assert oa.is_asy
        assert oa.flavor_family == "asy"
        assert oa.hqnumber == 4

        # check heavylight
        ohl = o.apply_flavor(on.heavylights[o.hqnumber - 4])
        assert ohl.hqnumber == o.hqnumber
        assert ohl.raw_flavor == o.raw_flavor
