import pytest
from eko.matchings import Atlas
from test_nc_n3lo_color_fact import MockCouplingConstants as MockCC

from yadism import observable_name as on
from yadism.coefficient_functions.fonll import kernels as aker
from yadism.coefficient_functions.heavy import kernels as hker
from yadism.coefficient_functions.intrinsic import kernels as iker
from yadism.coefficient_functions.light import kernels as lker


class MockCouplingConstants(MockCC):
    def get_weight(self, _pid, _q2, qct):
        if qct == "VV":
            return 1
        if qct == "VA":
            return 2
        if qct == "AV":
            return 4
        if qct == "AA":
            return 8
        raise ValueError(f"Unkown {qct}")


class MockSF:
    def __init__(self, n):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants()
        self.m2hq = [1.0, 2.0, 3.0]
        self.threshold = Atlas(matching_scales=self.m2hq, origin=(1.65**2, 4))


class MockESF:
    def __init__(self, sf, x, Q2):
        self.info = MockSF(sf)
        self.x = x
        self.Q2 = Q2
        self.process = "NC"


def mkpids(nf):
    """-nf ... 1 + 1 ... nf"""
    return list(range(-nf, 0)) + list(range(1, nf + 1))


def mkpc(nf, w):  # pc = parity conserving
    return dict(zip(mkpids(nf), [w] * 2 * nf))


def mkpv(nf, w):  # pv = parity violating
    return dict(zip(mkpids(nf), ([-w] * nf) + ([w] * nf)))


def check(ps, w):
    assert len(w) == len(ps)
    for e, k in zip(ps, w):
        assert e == k.partons


def test_generate_light_pc():
    esf = MockESF("F2_light", 0.1, 10)
    for nf in [3, 5]:
        w = lker.generate(esf, nf)
        # ns, g, s
        ps = [mkpc(nf, 9), {21: 9}, mkpc(nf, 9)]
        check(ps, w)


def test_generate_light_pv():  # pc = parity violating
    esf = MockESF("F3_light", 0.1, 10)
    for nf in [3, 5]:
        w = lker.generate(esf, nf)
        # ns, g, s
        ps = [mkpv(nf, 6), {21: 0}, mkpv(nf, 0)]
        check(ps, w)


def test_generate_heavy():
    esf = MockESF("F2_bottom", 0.1, 10)
    ihq = 5
    for nf in [3, 5]:
        w = hker.generate(esf, nf, ihq=ihq)
        # gVV, gAA, sVV, sAA
        ps = [{21: 1}, {21: 8}, mkpc(nf, 1), mkpc(nf, 8)]
        check(ps, w)


@pytest.mark.skip
def test_generate_light_fonll_diff_pc():
    esf = MockESF("F2_light", 0.1, 10)
    for nl in [3, 5]:
        w = aker.generate_light_asy(esf, nl)
        # c/t as light
        # TODO check values
        ps = [{-(nl + 1): 6.75 if nl == 3 else 7.5, (nl + 1): 6.75 if nl == 3 else 7.5}]
        check(ps, w)


@pytest.mark.skip
def test_generate_light_fonll_diff_pv():
    esf = MockESF("F3_light", 0.1, 10)
    for nl in [3, 5]:
        w = aker.generate_light_asy(esf, nl)
        # c/t as light
        ps = [{-(nl + 1): 0, (nl + 1): 0}]
        check(ps, w)


@pytest.mark.skip
def test_generate_heavy_fonll_diff_pc():
    esf = MockESF("F2_charm", 0.1, 10)
    for nl in [3, 5]:
        w = aker.generate_heavy_asy(esf, nl)
        # light part + asy
        ps = [
            {-(nl + 1): 9, (nl + 1): 9},
            {21: 9 / (nl + 1)},
            mkpc(nl, 9 / (nl + 1)),
            {21: -1},
            {21: -8},
            mkpc(nl, -1),
            mkpc(nl, -8),
        ]
        check(ps, w)


@pytest.mark.skip
def test_generate_heavy_fonll_diff_pv():
    esf = MockESF("F3_charm", 0.1, 10)
    for nl in [3, 5]:
        w = aker.generate_heavy_asy(esf, nl)
        # light part + asy
        ps = [{-(nl + 1): -6, (nl + 1): 6}, {21: 0}, mkpv(nl, 0)]
        check(ps, w)


def test_generate_intrinsic_pc():
    esf = MockESF("F2_charm", 0.1, 10)
    for nhq in [3, 5]:
        w = iker.generate(esf, nhq)
        # Sp, Sm
        ps = [{-nhq: 9, nhq: 9}, {-nhq: -7, nhq: -7}]
        check(ps, w)


def test_generate_intrinsic_pv():
    esf = MockESF("F3_charm", 0.1, 10)
    for nhq in [3, 5]:
        w = iker.generate(esf, nhq)
        # Rp, Rm
        ps = [{-nhq: -6, nhq: 6}, {-nhq: 2, nhq: -2}]
        check(ps, w)
