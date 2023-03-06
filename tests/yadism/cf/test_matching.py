import numba as nb
import numpy as np
from eko import constants, interpolation
from eko.mellin import Path
from ekore.harmonics import compute_cache
from ekore.operator_matrix_elements.unpolarized.space_like import as2
from numpy.testing import assert_allclose
from scipy.integrate import quad
from test_pc_general import MockESF

from yadism.coefficient_functions.fonll.partonic_channel import (
    K_qq_loc,
    K_qq_sing,
    PdfMatchingNNLLNonSinglet,
)
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
def yad_convolute(x, q):
    esf = MockESF(x, q**2)
    match = PdfMatchingNNLLNonSinglet(esf, nf, m2hq=q**2).NNLO()
    loc = match.loc(x, match.args["loc"]) * f(x)
    sing = quad(
        lambda z: match.sing(z, match.args["sing"]) * (f(x / z) / z - f(x)),
        x,
        1,
    )[0]
    return sing + loc


# n-space convolution
def inverse_mellin(x):
    def quad_ker_talbot(u, func):
        path = Path(u, np.log(x), True)
        sx = compute_cache(path.n, 3, True)
        sx = [np.array(s) for s in sx]
        integrand = path.prefactor * x ** (-path.n) * path.jac
        gamma = func(path.n, sx, L=0) * mellin_f(path.n)
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

    def test_nnlo(self):
        my = []
        eko = []
        for q in self.Qs:
            for x in self.xs:
                my.append(yad_convolute(x, q))
                eko.append(inverse_mellin(x))
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
    old = RSL(sing=K_qq_sing, loc=K_qq_loc, args=[])
    buza = RSL(reg=K_qq_reg_Buza, sing=K_qq_sing_Buza, loc=K_qq_loc_Buza, args=[1.0])
    xg = interpolation.lambertgrid(60)
    ipd = interpolation.InterpolatorDispatcher(xg, 4, mode_N=False)
    xb = 1e-5
    old_conv = conv.convolute_vector(old, ipd, xb)
    new_conv = conv.convolute_vector(buza, ipd, xb)
    np.testing.assert_allclose(old_conv[0], new_conv[0])
