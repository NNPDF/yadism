import numba as nb
import numpy as np

from .zeta import zeta2, zeta3

_P = (
    0.9999999999999999502e0,
    -2.6883926818565423430e0,
    2.6477222699473109692e0,
    -1.1538559607887416355e0,
    2.0886077795020607837e-1,
    -1.0859777134152463084e-2,
)
_Q = (
    1.0,
    -2.9383926818565635485e0,
    3.2712093293018635389e0,
    -1.7076702173954289421e0,
    4.1596017228400603836e-1,
    -3.9801343754084482956e-2,
    8.2743668974466659035e-4,
)
_PI = 3.14159265358979323846
_PI_SQ_OVER_6 = _PI * _PI / 6.0
_PI_SQ_OVER_12 = _PI * _PI / 12.0
_PI_SQ_OVER_3 = _PI * _PI / 3.0


@nb.njit(cache=True)
def li2(X):
    r"""Real dilogarithm :math:`Li_2(x)`.

    Implemented using an economized rational function approximation with
    a maximum error of :math:`5 \times 10^{-17}` following
    :cite:`Voigt:2022taz`.

    Note
    ----
    This is the dilog (:math:`Li_2(x)`) and *not* the Spence's function
    (:data:`scipy.special.spence`).

    Parameters
    ----------
    X : float
        argument of :math:`Li_2(x)`

    Returns
    -------
    float
        :math:`Li_2(x)`
    """
    if X < -1.0:
        l = np.log(1.0 - X)
        y = 1.0 / (1.0 - X)
        r = -_PI_SQ_OVER_6 + l * (0.5 * l - np.log(-X))
        s = 1.0
    elif X == -1.0:
        return -_PI_SQ_OVER_12
    elif X < 0.0:
        l = np.log1p(-X)
        y = X / (X - 1.0)
        r = -0.5 * l * l
        s = -1.0
    elif X == 0.0:
        return 0.0
    elif X < 0.5:
        y = X
        r = 0.0
        s = 1.0
    elif X < 1.0:
        y = 1.0 - X
        r = _PI_SQ_OVER_6 - np.log(X) * np.log1p(-X)
        s = -1.0
    elif X == 1.0:
        return _PI_SQ_OVER_6
    elif X < 2.0:
        l = np.log(X)
        y = 1.0 - 1.0 / X
        r = _PI_SQ_OVER_6 - l * (np.log(y) + 0.5 * l)
        s = 1.0
    else:
        l = np.log(X)
        y = 1.0 / X
        r = _PI_SQ_OVER_3 - 0.5 * l * l
        s = -1.0

    y2 = y * y
    y4 = y2 * y2
    p = _P[0] + y * _P[1] + y2 * (_P[2] + y * _P[3]) + y4 * (_P[4] + y * _P[5])
    q = (
        _Q[0]
        + y * _Q[1]
        + y2 * (_Q[2] + y * _Q[3])
        + y4 * (_Q[4] + y * _Q[5] + y2 * _Q[6])
    )

    return r + s * y * p / q


@nb.njit(cache=True)
def s2(z):
    x = z

    lnx = np.log(x)
    ddilog = li2

    S2 = -2 * ddilog(-x) + lnx**2 / 2 - 2 * lnx * np.log(1 + x) - np.pi**2 / 6

    return S2
