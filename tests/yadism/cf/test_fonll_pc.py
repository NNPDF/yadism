import numba as nb
import numpy as np
from eko import constants, interpolation

from yadism.coefficient_functions.fonll.partonic_channel import (
    K_qq_loc,
    K_qq_reg,
    K_qq_sing,
)
from yadism.coefficient_functions.partonic_channel import RSL
from yadism.coefficient_functions.special import li2
from yadism.coefficient_functions.special.nielsen import nielsen
from yadism.esf import conv


@nb.njit("f8(f8, f8[:])", cache=True)
def K_qq_sing_old(z, _args):
    """
    |ref| implements :eqref:`100`, :cite:`forte-fonll`.

    Parameters
    ----------
        z : float
            parton momentum

    Returns
    -------
        singular part of : math:`K_qq(z)`
    """
    as_norm = 4.0
    return (
        constants.CF
        * constants.TR
        * (
            (1.0 + z**2)
            / (1.0 - z)
            * (1.0 / 6.0 * np.log(z) ** 2 + 5.0 / 9.0 * np.log(z) + 28.0 / 27.0)
            + (1.0 - z) * (2.0 / 3.0 * np.log(z) + 13.0 / 9.0)
        )
        * as_norm
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def K_qq_loc_old(x, _args):
    """
    |ref| implements :eqref:`100`, :cite:`forte-fonll`.

    Parameters
    ----------
        x : float
            Bjorken x

    Returns
    -------
        local part of : math:`K_qq(z)`
    """
    as_norm = 4.0
    # Integrate[(1+z^2)/(1-z)(1/6 Log[z]^2+5/9Log[z]+28/27)+(1-z)(2/3Log[z]+13/9),{z,0,x},Assumptions->{0<x<1}]
    return (
        constants.CF
        * constants.TR
        * (
            -40 * np.pi**2
            - x * (8 + 211 * x)
            - 6
            * np.log(x)
            * (4 * np.pi**2 + x * (-16 + 19 * x) + 3 * x * (2 + x) * np.log(x))
            + 8 * np.log(1 - x) * (-56 + 9 * np.log(x) ** 2)
            + 48 * (5 + 3 * np.log(x)) * li2(1 - x)
            + 144 * nielsen(2, 1, x).real
        )
        / 216.0
        * as_norm
    )


def test_K_qq():
    old = RSL(sing=K_qq_sing_old, loc=K_qq_loc_old, args=[])
    new = RSL(reg=K_qq_reg, sing=K_qq_sing, loc=K_qq_loc, args=[1.0])
    xg = interpolation.make_lambert_grid(60)
    ipd = interpolation.InterpolatorDispatcher(xg, 4, mode_N=False)
    xb = 1e-5
    old_conv = conv.convolute_vector(old, ipd, xb)
    new_conv = conv.convolute_vector(new, ipd, xb)
    np.testing.assert_allclose(old_conv[0], new_conv[0], rtol=2e-4)
