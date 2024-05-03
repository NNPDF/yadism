import pytest

from yadism import observable_name as on
from yadism.coefficient_functions.asy import kernels as aker
from yadism.coefficient_functions.heavy import kernels as hker
from yadism.coefficient_functions.light import kernels as lker

from .test_nc_kernels import check, mkpids
from .test_nc_kernels import mkpc as mkpc_even
from .test_nc_kernels import mkpv as mkpv_odd


class MockCouplingConstants:
    def __init__(self, projectilePID):
        self.obs_config = dict(projectilePID=projectilePID)

    def get_weight(self, _pid, _q2, _qct, cc_mask):
        r = 0
        if "dus" in cc_mask:
            r += 1
        if "c" in cc_mask:
            r += 2
        if "b" in cc_mask:
            r += 4
        if "t" in cc_mask:
            r += 8
        return r


class MockSF:
    def __init__(self, n, projectilePID):
        self.obs_name = on.ObservableName(n)
        self.coupling_constants = MockCouplingConstants(projectilePID)
        self.m2hq = [1.0, 2.0, 3.0]


class MockESF:
    def __init__(self, sf, projectilePID, x, Q2):
        self.info = MockSF(sf, projectilePID)
        self.x = x
        self.Q2 = Q2
        self.process = "CC"



def mkpc_odd(nf, w, sgn):  # pc = parity conserving
    return dict(
        zip(
            mkpids(nf),
            [(-1) ** (j + (1 if not sgn else 0)) * w for j in range(nf)]
            + [(-1) ** (j + (1 if sgn else 0)) * w for j in range(nf)],
        )
    )


def mkpv_even(nf, w, sgn):  # pv = parity violating
    return dict(
        zip(
            mkpids(nf),
            [(-1) ** (j + (1 if sgn else 0)) * w for j in range(nf)]
            + [(-1) ** (j + (1 if sgn else 0)) * w for j in range(nf)],
        )
    )

def mkpv_valence(nf, w):  # pv = parity violating
    return dict(
        zip(
            mkpids(nf),
            [(-1) ** (j + 1) * w for j in range(nf)]
            + [(-1) ** (j) * w for j in range(nf)],
        )
    )

def test_generate_light_pc():
    for sgn in [True, False]:
        esf = MockESF("F2_light", 11 * (1 if sgn else -1), 0.1, 10)
        for nf in [3, 5]:
            w = lker.generate(esf, nf)
            norm = {3: 1, 4: 3, 5: 7}[nf]
            # q, g
            ps = [
                mkpc_even(nf, 0.5 * norm),
                {21: (nf + 1) * norm / nf / 2.0},
                mkpc_even(nf, (nf + 1) * norm / nf / 2.0),
                mkpc_odd(nf, 0.5 * norm, sgn),
            ]
            check(ps, w)


def test_generate_light_pv():
    for sgn in [True, False]:
        esf = MockESF("F3_light", 11 * (1 if sgn else -1), 0.1, 10)
        for nf in [3, 5]:
            w = lker.generate(esf, nf)
            norm = {3: 1, 4: 3, 5: 7}[nf]
            # q, g
            ps = [
                mkpv_even(nf, 0.5 * norm, sgn),
                mkpv_odd(nf, 0.5 * norm),
                mkpv_valence(nf, (nf + 1) * norm / nf / 2.0),
            ]
            check(ps, w)


# def test_generate_heavy_pc():
#     for sgn in [True, False]:
#         esf = MockESF("F2_charm", 11 * (1 if sgn else -1), 0.1, 10)
#         for nf in [3, 4, 5]:
#             w = hker.generate(esf, nf)
#             qnorm = {3: 2, 4: 4, 5: 8}[nf]
#             gnorm = {3: 4, 4: 10, 5: 24}[nf]
#             # q, g
#             ps = [mkpc(nf, qnorm, sgn), {21: gnorm}]
#             check(ps, w)


# def test_generate_heavy_pv():
#     for sgn in [True, False]:
#         esf = MockESF("F3_charm", 11 * (1 if sgn else -1), 0.1, 10)
#         for nf in [3, 4, 5]:
#             w = hker.generate(esf, nf)
#             qnorm = {3: 2, 4: 4, 5: 8}[nf]
#             gnorm = {3: 4, 4: 10, 5: 24}[nf]
#             # q, g
#             ps = [mkpv(nf, qnorm, sgn), {21: (-1 if sgn else 1) * gnorm}]
#             check(ps, w)


# def test_generate_light_fonll_diff():
#     for sgn in [True, False]:
#         for esf in [
#             MockESF("F2_light", 11 * (1 if sgn else -1), 0.1, 10),
#             MockESF("F3_light", 11 * (1 if sgn else -1), 0.1, 10),
#         ]:
#             for nf in [3, 4, 5]:
#                 w = aker.generate_light_asy(esf, nf)
#                 # TODO fix
#                 qnorm = {3: 2.5 / 3, 4: 2.25, 5: 4.2}[nf]
#                 kindsgn = esf.sf.obs_name.kind == "F3"
#                 ps = [
#                     {
#                         nf + 1: (1 if kindsgn != sgn else -1) * qnorm,
#                         -(nf + 1): (1 if kindsgn != sgn else -1) * qnorm,
#                     }
#                 ]
#                 check(ps, w)


# def test_generate_heavy_fonll_diff_pc():
#     for sgn in [True, False]:
#         esf = MockESF("F2charm", 11 * (1 if sgn else -1), 0.1, 10)
#         for nl in [3, 4, 5]:
#             w = kernels.generate_heavy_asy(esf, nl)
#             norm = {3: 2, 4: 4, 5: 8}[nl]
#             # light - asy
#             ps = [
#                 mkpc(nl+1, norm, sgn),
#                 {21: norm  / 2.0},
#                 {(nl+1): 1},
#                 {21: -1}
#             ]
#             check(ps, w)
