import numpy as np
import pytest

from yadism.esf.result import ESFResult, EXSResult

lo = (0, 0, 0, 0)


class MockPDFgonly:
    def hasFlavor(self, pid):
        return pid == 21

    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x**2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


class TestESFResult:
    def test_from_document(self):
        d = dict(
            x=0.5,
            Q2=10,
            orders=[
                dict(
                    order=list(lo),
                    values=np.random.rand(2, 2),
                    errors=np.random.rand(2, 2),
                )
            ],
            nf=3,
        )
        r = ESFResult.from_document(d)
        assert len(list(r.orders.values())[0]) == len(d["orders"][0]["values"])

        rr = ESFResult.from_document(r.get_raw())
        assert len(list(rr.orders.values())[0]) == len(d["orders"][0]["values"])

    def test_get_raw(self):
        a = dict(
            x=0.5,
            Q2=10,
            orders={lo: (np.random.rand(2, 2), np.random.rand(2, 2))},
            nf=4,
        )

        ra = ESFResult(**a)
        dra = ra.get_raw()
        rb = ESFResult.from_document(dra)
        # they should be just the very same!
        assert ra.x == rb.x
        assert ra.Q2 == rb.Q2
        for aa, bb in zip(ra.orders.values(), rb.orders.values()):
            for k in [0, 1]:
                assert pytest.approx(aa[k]) == bb[k]

    def test_mul(self):
        v, e = np.random.rand(2, 2, 2)
        r = ESFResult(**dict(x=0.1, Q2=10, orders={lo: (v, e)}, nf=5))
        for x in [2.0, (2.0, 0.0)]:
            rm = r * x
            np.testing.assert_allclose(rm.orders[lo][0], 2.0 * v)
            np.testing.assert_allclose(rm.orders[lo][1], 2.0 * e)
            rmul = x * r
            np.testing.assert_allclose(rmul.orders[lo][0], 2.0 * v)
            np.testing.assert_allclose(rmul.orders[lo][1], 2.0 * e)
        with pytest.raises(IndexError):
            _rm = r * (2,)

        y = (2.0, 2.0)
        rm = r * y
        np.testing.assert_allclose(rm.orders[lo][0], 2.0 * v)
        np.testing.assert_allclose(rm.orders[lo][1], 2.0 * (v + e))

    def test_add(self):
        va, vb, ea, eb = np.random.rand(4, 2, 2)
        ra = ESFResult(**dict(x=0.1, Q2=10, orders={lo: (va, ea)}, nf=6))
        rb = ESFResult(**dict(x=0.1, Q2=10, orders={lo: (vb, eb)}, nf=3))
        radd = ra + rb
        np.testing.assert_allclose(radd.orders[lo][0], va + vb)
        np.testing.assert_allclose(radd.orders[lo][1], ea + eb)
        raa = ESFResult(**dict(x=0.1, Q2=10, orders={lo: (va, ea)}, nf=5))
        r2a = ra + raa
        np.testing.assert_allclose(r2a.orders[lo][0], 2.0 * va)
        np.testing.assert_allclose(r2a.orders[lo][1], 2.0 * ea)

    def test_apply_pdf(self):
        # test Q2 values
        for Q2 in [1, 10, 100]:
            a = dict(
                x=0.5, Q2=Q2, orders={lo: ([[1, 0], [0, 1]], [[1, 0], [0, 1]])}, nf=6
            )
            # plain
            ra = ESFResult(**a)
            pra = ra.apply_pdf(
                MockPDFgonly(),
                [21, 1],
                [0.5, 1.0],
                lambda _muR: 1.0,
                lambda _muR: 1.0,
                1.0,
                1.0,
            )
            expexted_res = a["orders"][lo][0][0][0] * a["x"] * a["Q2"]
            expected_err = np.abs(a["orders"][lo][1][0][0]) * a["x"] * a["Q2"]
            assert pytest.approx(pra["result"], 0, 0) == expexted_res
            assert pytest.approx(pra["error"], 0, 0) == expected_err
            # test factorization scale variation
            for xiF in [0.5, 2.0]:
                pra = ra.apply_pdf(
                    MockPDFgonly(),
                    [21, 1],
                    [0.5, 1.0],
                    lambda _muR: 1.0,
                    lambda _muR: 1.0,
                    1.0,
                    xiF,
                )
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF**2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF**2

        # errors
        with pytest.raises(ValueError, match=r"Q2"):
            a = dict(
                x=0.5, Q2="bla", orders={lo: ([[1, 0], [0, 1]], [[1, 0], [0, 1]])}, nf=3
            )

            ra = ESFResult(**a)
            ra.apply_pdf(
                MockPDFgonly(),
                [21, 1],
                [0.5, 1.0],
                lambda _muR: 1.0,
                lambda _muR: 1.0,
                1.0,
                1.0,
            )


class TestEXSResult:
    def test_from_document(self):
        d = dict(
            x=0.5,
            Q2=10,
            orders=[
                dict(
                    order=list(lo),
                    values=np.random.rand(2, 2),
                    errors=np.random.rand(2, 2),
                )
            ],
            nf=3,
        )
        with pytest.raises(KeyError, match="y"):
            _missing_y = EXSResult.from_document(d)
        d["y"] = 0.123
        r = EXSResult.from_document(d)
        assert len(list(r.orders.values())[0]) == len(d["orders"][0]["values"])
        assert r.y == 0.123

        rr = EXSResult.from_document(r.get_raw())
        assert len(list(rr.orders.values())[0]) == len(d["orders"][0]["values"])
        assert rr.y == 0.123
