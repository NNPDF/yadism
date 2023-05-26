import numba as nb
import numpy as np
from eko import constants, interpolation
from eko.mellin import Path
from ekore.harmonics import cache
from ekore.operator_matrix_elements.unpolarized.space_like import as2 as as2_pol
from ekore.operator_matrix_elements.unpolarized.space_like import as2 as as2_unp
from numpy.testing import assert_allclose
from scipy.integrate import quad
from test_pc_general import MockESF

from yadism.coefficient_functions.fonll import partonic_channel as pc
from yadism.coefficient_functions.partonic_channel import RSL
from yadism.coefficient_functions.special import zeta
from yadism.esf import conv

nf = 4
mhq = 1.51


# a simple test function  and its mellin transform
def f(x):
    return x * (1 - x)


def mellin_f(n):
    return 1 / (2 + 3 * n + n**2)


# x-space convolution
def yad_convolute(x, q, pc):
    esf = MockESF(x, q**2)
    result = 0
    for matchfunc in [
        pc.PdfMatchingNNLLNonSinglet,
        pc.PdfMatchingNLLNonSinglet,
        pc.PdfMatchingLLNonSinglet,
    ]:
        match = matchfunc(esf, nf, m2hq=mhq**2).NNLO()
        loc = match.loc(x, match.args["loc"]) * f(x)
        sing = quad(
            lambda z: match.sing(z, match.args["sing"]) * (f(x / z) / z - f(x)),
            x,
            1,
        )[0]
        reg = 0
        if match.reg is not None:
            reg = quad(
                lambda z: match.reg(z, match.args["reg"]) * f(x / z) / z,
                x,
                1,
            )[0]
        result += sing + loc + reg
    return result


# n-space convolution
def inverse_mellin(x, q, as2):
    def quad_ker_talbot(u, func):
        path = Path(u, np.log(x), True)
        sx_cache = cache.reset()
        integrand = path.prefactor * x ** (-path.n) * path.jac
        gamma = func(path.n, sx_cache, L=np.log(q**2 / mhq**2)) * mellin_f(path.n)
        return np.real(gamma * integrand)

    return quad(
        lambda u: quad_ker_talbot(u, as2.A_qq_ns),
        0.5,
        1.0,
        epsabs=1e-12,
        epsrel=1e-6,
        limit=200,
        full_output=1,
    )[0]


class Test_Matching_qq:
    xs = [0.0001, 0.001, 0.01, 0.1, 0.2, 0.456, 0.7]
    Qs = [5, 10, 20]

    def test_nnlo_unpolarized(self):
        my = []
        eko = []
        for q in self.Qs:
            for x in self.xs:
                my.append(yad_convolute(x, q, pc))
                eko.append(inverse_mellin(x, q, as2_unp))
        assert_allclose(my, eko)

    def test_nnlo_polarized(self):
        my = []
        eko = []
        for q in self.Qs:
            for x in self.xs:
                my.append(yad_convolute(x, q, pc))
                eko.append(inverse_mellin(x, q, as2_pol))
        assert_allclose(my, eko)


@nb.njit("f8(f8, f8[:])", cache=True)
def K_qq_reg_Buza(z, args):
    """
    |ref| implements :eqref:`B.4`, :cite:`Buza:1996wv`.
    Parameters
    ----------
        z : float
            parton momentum
    Returns
    -------
        regular part of : math:`K_qq(z)`
    """
    k = np.log(args[0])
    return (
        constants.CF
        * constants.TR
        * (
            (
                ((1.0 + z**2) / (1.0 - z))
                * (2.0 / 3.0 * np.log(z) ** 2 + 20.0 / 9.0 * np.log(z))
                + (8.0 / 3.0 * (1.0 - z) * np.log(z))
                + 44.0 / 27.0
                - 268.0 / 27.0 * z
            )
            + (
                (8.0 / 3.0) * ((1.0 + z**2) / (1.0 - z)) * np.log(z)
                + 8.0 / 9.0
                - 88.0 / 9.0 * z
            )
            * (-k)
            + (-4.0 / 3.0 - 4.0 / 3.0 * z) * (-k) ** 2
        )
    )


@nb.njit("f8(f8[:])", cache=True)
def K_qq_omx_Buza(args):
    """
    |ref| implements :eqref:`B.4`, :cite:`Buza:1996wv`.
    Parameters
    ----------
        z : float
            parton momentum
    Returns
    -------
        1/(1-z) part of : math:`K_qq(z)`
    """
    k = np.log(args[0])
    return 224.0 / 27.0 + 80.0 / 9.0 * (-k) + 8.0 / 3.0 * (-k) ** 2


@nb.njit("f8(f8,f8[:])", cache=True)
def K_qq_sing_Buza(z, args):
    """
    |ref| implements :eqref:`B.4`, :cite:`Buza:1996wv`.
    Parameters
    ----------
        z : float
            parton momentum
    Returns
    -------
        singular part of : math:`K_qq(z)`
    """
    return constants.CF * constants.TR * (K_qq_omx_Buza(args) / (1.0 - z))


@nb.njit("f8(f8,f8[:])", cache=True)
def K_qq_loc_Buza(x, args):
    """
    |ref| implements :eqref:`B.4`, :cite:`Buza:1996wv`.
    Parameters
    ----------
        x : float
            Bjorken x
    Returns
    -------
        local part of : math:`K_qq(z)`
    """
    k = np.log(args[0])
    return (
        constants.CF
        * constants.TR
        * (
            (-8.0 / 3.0 * zeta.zeta3 + 40.0 / 9.0 * zeta.zeta2 + 73.0 / 18.0)
            + (16.0 / 3.0 * zeta.zeta2 + 2.0 / 3.0) * (-k)
            + 2.0 * (-k) ** 2
            + K_qq_omx_Buza(args) * np.log(1.0 - x)
        )
    )


def test_K_qq():
    old = RSL(sing=pc.K_qq_sing, loc=pc.K_qq_loc, args=[])
    buza = RSL(reg=K_qq_reg_Buza, sing=K_qq_sing_Buza, loc=K_qq_loc_Buza, args=[1.0])
    xg = interpolation.lambertgrid(60)
    ipd = interpolation.InterpolatorDispatcher(xg, 4, mode_N=False)
    xb = 1e-5
    old_conv = conv.convolute_vector(old, ipd, xb)
    new_conv = conv.convolute_vector(buza, ipd, xb)
    np.testing.assert_allclose(old_conv[0], new_conv[0])
