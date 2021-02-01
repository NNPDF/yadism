# -*- coding: utf-8 -*-
import copy

import numpy as np
import pytest

from yadism.esf.esf_result import ESFResult


class MockPDFgonly:
    def hasFlavor(self, pid):
        return pid == 21

    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x ** 2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


class TestESFResult:
    def test_from_dict(self):
        d = dict(
            x=0.5,
            Q2=10,
            values=np.random.rand(2, 2),
            errors=np.random.rand(2, 2),
        )
        r = ESFResult.from_dict(d)
        assert len(r.values) == len(d["values"])

    def test_get_raw(self):
        a = dict(
            x=0.5,
            Q2=10,
            values=np.random.rand(2, 2),
            errors=np.random.rand(2, 2),
        )

        ra = ESFResult.from_dict(a)
        dra = ra.get_raw()
        # they should be just the very same!
        for k, v in a.items():
            assert k in dra
            assert pytest.approx(v) == dra[k]

    def test_mul(self):
        v, e = np.random.rand(2, 2, 2)
        r = ESFResult.from_dict(dict(x=0.1, Q2=10, values=v, errors=e))
        for x in [2.0, (2.0, 0.0)]:
            rm = r * x
            np.testing.assert_allclose(rm.values, 2.0 * v)
            np.testing.assert_allclose(rm.errors, 2.0 * e)
            rmul = x * r
            np.testing.assert_allclose(rmul.values, 2.0 * v)
            np.testing.assert_allclose(rmul.errors, 2.0 * e)
        with pytest.raises(IndexError):
            _rm = r * (2,)

        y = (2.0, 2.0)
        rm = r * y
        np.testing.assert_allclose(rm.values, 2.0 * v)
        np.testing.assert_allclose(rm.errors, 2.0 * (v + e))

    def test_add(self):
        va, vb, ea, eb = np.random.rand(4, 2, 2)
        ra = ESFResult.from_dict(dict(x=0.1, Q2=10, values=va, errors=ea))
        rb = ESFResult.from_dict(dict(x=0.1, Q2=10, values=vb, errors=eb))
        radd = ra + rb
        np.testing.assert_allclose(radd.values, va + vb)
        np.testing.assert_allclose(radd.errors, ea + eb)
        raa = ESFResult.from_dict(dict(x=0.1, Q2=10, values=va, errors=ea))
        r2a = ra + raa
        np.testing.assert_allclose(r2a.values, 2.0 * va)
        np.testing.assert_allclose(r2a.errors, 2.0 * ea)

    def test_apply_pdf(self):
        # test Q2 values
        for Q2 in [1, 10, 100]:
            a = dict(
                x=0.5,
                Q2=Q2,
                values=[[1, 0], [0, 1]],
                errors=[[1, 0], [0, 1]],
            )
            # plain
            ra = ESFResult.from_dict(a)
            pra = ra.apply_pdf(MockPDFgonly(), [21, 1], [0.5, 1.0], 1.0)
            expexted_res = a["values"][0][0] * a["x"] * a["Q2"]
            expected_err = np.abs(a["values"][0][0]) * a["x"] * a["Q2"]
            assert pytest.approx(pra["result"], 0, 0) == expexted_res
            assert pytest.approx(pra["error"], 0, 0) == expected_err
            # test factorization scale variation
            for xiF in [0.5, 2.0]:
                pra = ra.apply_pdf(MockPDFgonly(), [21, 1], [0.5, 1.0], xiF)
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF ** 2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF ** 2

        # errors
        with pytest.raises(ValueError, match=r"Q2"):
            a = dict(
                x=0.5,
                Q2="bla",
                values=np.random.rand(2, 2),
                errors=np.random.rand(2, 2),
            )

            ra = ESFResult.from_dict(a)
            ra.apply_pdf(MockPDFgonly(), [21, 1], [0.5, 1.0], 1.0)
