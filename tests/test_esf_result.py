# -*- coding: utf-8 -*-
import copy

import numpy as np
import pytest

from yadism.structure_functions.esf_result import ESFResult


class MockPDFgonly:
    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x ** 2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


@pytest.mark.quick_check
class TestESFResult:
    def test_init(self):
        # test creation
        for x in [0.1, 0.2]:
            r = ESFResult(x)
            assert r.x == x

    def test_from_dict(self):
        d = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[0, 1], g=[1, 0]),
            errors=dict(q=[0, 0], g=[0, 0]),
        )
        dt = np.float
        r = ESFResult.from_dict(d, dt)
        assert len(r.values["q"]) == len(d["values"]["q"])
        assert isinstance(r.values["q"][0], dt)

    def test_add(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[0, 1], g=[1, 0]),
            errors=dict(q=[0, 0], g=[0, 0]),
        )
        b = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[1, 0], g=[0, 1]),
            errors=dict(q=[1, 1], g=[1, 1]),
        )

        ra = ESFResult.from_dict(a)
        rb = ESFResult.from_dict(b)

        # sum
        rc = ra + rb
        assert pytest.approx(rc.values["q"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 1])

        # subtract
        rc1 = ra - rb
        rc2 = copy.deepcopy(ra)
        rc2 -= rb
        for rc in [rc1, rc2]:
            assert pytest.approx(rc.values["q"], 0, 0) == np.array([-1, 1])
            assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 1])
            assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, -1])
            assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 1])

    def test_neg(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        rc = -ra

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, -1])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 0])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 0])

    def test_mul(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        rc = ra * 2

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 2])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([2, 0])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([-2, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([2, 0])

        rc = [2, 1] * ra

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 2])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([2, 1])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([-2, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([3, 0])

        rc1 = ra / 2.0
        rc2 = copy.deepcopy(ra)
        rc2 /= 2
        for rc in [rc1, rc2]:
            assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 0.5])
            assert pytest.approx(rc.errors["q"], 0, 0) == np.array([0.5, 0])
            assert pytest.approx(rc.values["g"], 0, 0) == np.array([-0.5, 0])
            assert pytest.approx(rc.errors["g"], 0, 0) == np.array([0.5, 0])

        with pytest.raises(ValueError):
            ra *= [1, 2, 3]

    def test_get_raw(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights={},
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        dra = ra.get_raw()
        # they should be just the very same!
        assert dra == a

    def test_apply_pdf(self):
        # test Q2 values
        for Q2 in [1, 10, 100]:
            a = dict(
                x=0.5,
                Q2=Q2,
                weights={"g": {21: 2 / 9}, "q": {}},
                values=dict(q=[0, 1], g=[-1, 0]),
                errors=dict(q=[1, 0], g=[1, 0]),
            )
            # plain
            ra = ESFResult.from_dict(a)
            pra = ra.apply_pdf([0.5, 1.0], 1.0, MockPDFgonly())
            expexted_res = a["values"]["g"][0] * a["x"] * a["Q2"] * 2 / 9
            expected_err = np.abs(a["values"]["g"][0]) * a["x"] * a["Q2"] * 2 / 9
            assert pytest.approx(pra["result"], 0, 0) == expexted_res
            assert pytest.approx(pra["error"], 0, 0) == expected_err
            # test factorization scale variation
            for xiF in [0.5, 2.0]:
                pra = ra.apply_pdf([0.5, 1.0], xiF, MockPDFgonly())
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF ** 2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF ** 2

        # errors
        with pytest.raises(ValueError, match=r"Q2"):
            r = ESFResult()
            r.apply_pdf([1, 2, 3], 1, MockPDFgonly())
