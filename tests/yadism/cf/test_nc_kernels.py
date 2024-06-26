import numpy as np
import pytest
from eko.matchings import Atlas

from yadism import observable_name as on
from yadism.coefficient_functions import coupling_constants as cc
from yadism.coefficient_functions.asy import kernels as aker
from yadism.coefficient_functions.heavy import kernels as hker
from yadism.coefficient_functions.intrinsic import kernels as iker
from yadism.coefficient_functions.light import kernels as lker


class MockCouplingConstants:

    def __init__(self):
        self.charges = {pid: np.random.rand() for pid in range(1, 7)}

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

    def get_fl11_weight(self, _pid, _q2, _nf, qct):
        return self.get_weight(_pid, _q2, qct)


class MockSF:
    def __init__(self, n):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants()
        self.m2hq = [1.0, 2.0, 3.0]
        self.threshold = Atlas(matching_scales=self.m2hq, origin=(1.65**2, 4))
        self.theory = {"n3lo_cf_variation": 0, "pto": 3}


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
        # ns, g, s, fl11ns, fl11g, fl11ps
        ps = [mkpc(nf, 9), {21: 9}, mkpc(nf, 9), mkpc(nf, 9), {21: 9}]
        check(ps, w)


def test_generate_light_pv():  # pc = parity violating
    esf = MockESF("F3_light", 0.1, 10)
    for nf in [3, 5]:
        w = lker.generate(esf, nf)
        # ns, v
        ps = [mkpv(nf, 6), mkpv(nf, 6)]
        check(ps, w)


def test_generate_heavy():
    esf = MockESF("F2_bottom", 0.1, 10)
    ihq = 5
    for nf in [3, 5]:
        w = hker.generate(esf, nf, ihq=ihq)
        # gVV, gAA, sVV, sAA
        ps = [{21: 1}, {21: 8}, mkpc(nf, 1), mkpc(nf, 8)]
        check(ps, w)


def test_nc_fl11_weights():
    # Test the the flavor decomposition of the fl11 diagrams is the same as we get from
    # the yadism implementation
    th_d = dict(
        SIN2TW=0.5,
        MZ=80,
        CKM="0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    )
    obs_d = dict(
        projectilePID=11,
        PolarizationDIS=0.0,
        prDIS="EM",
        PropagatorCorrection=0,
        NCPositivityCharge=None,
    )
    coupl_const = cc.CouplingConstants.from_dict(th_d, obs_d)

    Q2 = 1.0
    mean_e = 0
    mean_e2 = 0
    for nf in range(1, 7):
        fl11_weights = lker.nc_fl11_weights(coupl_const, Q2, nf)
        fl2_weights = lker.nc_weights(coupl_const, Q2, nf, False)

        # build ratios to fl2
        mean_e += coupl_const.electric_charge[nf]
        mean_e2 += coupl_const.electric_charge[nf] ** 2
        w3 = mean_e**2 / nf / mean_e2
        w2 = 3 * mean_e / nf

        # test gluon coupling
        np.testing.assert_allclose(fl11_weights["g"][21], fl2_weights["g"][21] * w3)

        # test the quark sector
        # now need to sum over all the pids
        q = 0
        ns = 0
        ps = 0
        for pid, c in fl11_weights["q"].items():
            ns += w2 * fl2_weights["ns"][pid]
            ps += (w3 - w2) * fl2_weights["s"][pid]
            q += c
        np.testing.assert_allclose(ns + ps, q)


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
