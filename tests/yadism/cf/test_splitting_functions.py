# -*- coding: utf-8 -*-
import numpy as np
from eko import interpolation
from eko.anomalous_dimensions import harmonics, lo, nlo
from scipy import integrate

from yadism.coefficient_functions import splitting_functions as sf
from yadism.esf import conv


def mellin_transform(rsl, N):
    """
    Mellin transformation

    Parameters
    ----------
        rsl : RSL
            integration kernel :math:`f(x)`
        N : complex
            transformation point

    Returns
    -------
        res : complex
            computed point
        err : complex
            error
    """

    def integrand_reg_sing(x):
        xToN = pow(x, N - 1) * rsl.reg(x, rsl.args["reg"]) + (
            pow(x, N - 1) - 1.0
        ) * rsl.sing(x, rsl.args["sing"])
        return xToN

    def integrand_reg(x):
        xToN = pow(x, N - 1) * rsl.reg(x, rsl.args["reg"])
        return xToN

    # do real + imaginary part seperately
    integrand = integrand_reg_sing
    if rsl.sing is None:
        integrand = integrand_reg
    r, re = integrate.quad(lambda x: np.real(integrand(x)), 0, 1, full_output=1)[:2]
    i, ie = integrate.quad(lambda x: np.imag(integrand(x)), 0, 1, full_output=1)[:2]
    if rsl.loc is not None:
        r += rsl.loc(0.0, rsl.args["loc"])
    result = complex(r, i)
    error = complex(re, ie)
    return result, error


class BenchmarkSFEKO:
    def benchmark_lo(self):
        for nf in [3, 4]:
            for n in [1.0 + 0j, 2.0 + 0j, 3.0 + 0j]:
                s1 = harmonics.harmonic_S1(n)
                # qq - gamma_qq(N=1)=0, so we need an atol
                y_qq = mellin_transform(sf.lo.pqq(nf), n)
                e_qq = -lo.gamma_ns_0(n, s1)
                np.testing.assert_allclose(y_qq[0], e_qq, atol=1e-6)
                # qg
                y_qg = mellin_transform(sf.lo.pqg(nf), n)
                e_qg = -lo.gamma_qg_0(n, nf)
                np.testing.assert_allclose(y_qg[0], e_qg)
                # protect singlet likes
                if np.abs(n - 1.0) > 1e-5:
                    # gq
                    y_gq = mellin_transform(sf.nlo.pgq0(nf), n)
                    e_gq = -lo.gamma_gq_0(n)
                    np.testing.assert_allclose(y_gq[0], e_gq)
                    # gg
                    y_gg = mellin_transform(sf.nlo.pgg0(nf), n)
                    e_gg = -lo.gamma_gg_0(n, s1, nf)
                    np.testing.assert_allclose(y_gg[0], e_gg)

    def benchmark_nlo(self):
        for nf in [3, 4]:
            for n in [1.0 + 0j, 2.0 + 0j, 3.0 + 0j]:
                # nsm
                y_nsm = mellin_transform(sf.nlo.pnsm1(nf), n)
                e_nsm = -nlo.gamma_nsm_1(n, nf)
                np.testing.assert_allclose(y_nsm[0], e_nsm, atol=2e-6)
                # nsp
                y_nsp = mellin_transform(sf.nlo.pnsp1(nf), n)
                e_nsp = -nlo.gamma_nsp_1(n, nf)
                np.testing.assert_allclose(y_nsp[0], e_nsp, atol=2e-6)
                # protect singlet likes
                if np.abs(n - 1.0) > 1e-5:
                    # qq
                    y_qq = mellin_transform(sf.nlo.pqq1(nf), n)
                    e_qq = -(nlo.gamma_nsp_1(n, nf) + nlo.gamma_ps_1(n, nf))
                    np.testing.assert_allclose(y_qq[0], e_qq, atol=1e-6)
                    # qg
                    y_qg = mellin_transform(sf.nlo.pqg1(nf), n)
                    e_qg = -nlo.gamma_qg_1(n, nf)
                    np.testing.assert_allclose(y_qg[0], e_qg)

    def benchmark_conv(self):
        for nf in [3, 4]:
            for n in [1.0 + 0j, 2.0 + 0j, 3.0 + 0j]:
                s1 = harmonics.harmonic_S1(n)
                # # qq*qq
                y_qqqq = mellin_transform(sf.nlo.pqq0_2(nf), n)
                e_qqqq = (-lo.gamma_ns_0(n, s1)) * (-lo.gamma_ns_0(n, s1))
                np.testing.assert_allclose(y_qqqq[0], e_qqqq, atol=1e-12)
                # qq*qg
                y_qqqg = mellin_transform(sf.nlo.pqq0pqg0(nf), n)
                e_qqqg = (-lo.gamma_ns_0(n, s1)) * (-lo.gamma_qg_0(n, nf))
                np.testing.assert_allclose(y_qqqg[0], e_qqqg, atol=1e-12)
                # protect singlet likes
                if np.abs(n - 1.0) > 1e-5:
                    # qg*gq
                    y_qggq = mellin_transform(sf.nlo.pqg0pgq0(nf), n)
                    e_qggq = (-lo.gamma_qg_0(n, nf)) * (-lo.gamma_gq_0(n))
                    np.testing.assert_allclose(y_qggq[0], e_qggq, atol=1e-12)
                    # qg*gg
                    y_qggg = mellin_transform(sf.nlo.pqg0pgg0(nf), n)
                    e_qggg = (-lo.gamma_qg_0(n, nf)) * (-lo.gamma_gg_0(n, s1, nf))
                    np.testing.assert_allclose(y_qggg[0], e_qggg, atol=1e-12)


# class TestConv:
#     def test_pqg0pgq0(self):
#         nf = 3
#         i = interpolation.InterpolatorDispatcher(interpolation.make_grid(30,20),4,mode_N=False)
#         o_pqg = conv.convolute_operator(sf.lo.pqg(nf), i)
#         o_pgq = conv.convolute_operator(sf.nlo.pgq0(nf),i)
#         o_pqg0pgq0 = conv.convolute_operator(sf.nlo.pqg0pgg0(nf),i)
#         np.testing.assert_allclose(o_pqg0pgq0[0], o_pqg[0] @ o_pgq[0])