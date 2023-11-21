"""
Note that here the m refers to odd-N, but it actually corresponds to
:math:`\nu + \bar{\nu}`. Vice versa for the minus combination.
To generate `c3np3a,c3np3c` we follow `xcdiff3p.f` or the reference paper :cite:`Davies:2016ruz`.
"""
import numba as nb
import numpy as np

from .common import d3, d27, d81, d243
from .xcdiff3p import c3q3dfp, c3q3dfpc


@nb.njit("f8(f8,f8[:])", cache=True)
def c3nm3a(y, args):
    nf = args[0]
    has_color_fact = args[1]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(1.0 - y)
    if has_color_fact:
        fl02 = 1.0
    else:
        fl02 = 0.0
    res = (
        -1853.0
        - 5709.0 * y
        + y * y1 * (5600.0 - 1432.0 * y)
        - 536.0 / 405.0 * dl**5
        - 4036.0 / 81.0 * dl**4
        - 496.95 * dl**3
        - 1488.0 * dl**2
        - 293.3 * dl
        - 512.0 * d27 * dl1**5
        + 8896.0 * d27 * dl1**4
        - 1396.0 * dl1**3
        + 3990.0 * dl1**2
        + 14363.0 * dl1
        - 0.463 * y * dl**6
        - dl * dl1 * (4007.0 + 1312.0 * dl)
        + nf
        * (
            516.1
            - 465.2 * y
            + y * y1 * (635.3 + 310.4 * y)
            + 304.0 / 81.0 * dl**4
            + 48512.0 / 729.0 * dl**3
            + 305.32 * dl**2
            + 366.9 * dl
            - 1.200 * y * dl**4
            - 640.0 / 81.0 * dl1**4
            + 32576.0 / 243.0 * dl1**3
            - 660.7 * dl1**2
            + 959.1 * dl1
            + 31.95 * (1.0 - y) * dl1**4
            + dl * dl1 * (1496.0 + 270.1 * dl - 1191.0 * dl1)
        )
        + nf**2
        * (
            11.32
            + 51.94 * y
            - y * y1 * (44.52 + 11.05 * y)
            - 368.0 * d243 * dl**3
            - 2848.0 / 243.0 * dl**2
            - 16.00 * dl
            - 64.0 / 81.0 * dl1**3
            + 992.0 / 81.0 * dl1**2
            - 49.65 * dl1
            - dl * dl1 * (39.99 + 5.103 * dl - 16.30 * dl1)
            + 0.0647 * y * dl**4
        )
        + fl02
        * nf
        * (
            48.79
            - (242.4 - 150.7 * y) * y1
            - 16.0 / 27.0 * dl**5
            + 17.26 * dl**3
            - 113.4 * dl**2
            - 477.0 * dl
            + 2.147 * dl1**2
            - 24.57 * dl1
            + y * dl * (218.1 + 82.27 * dl**2)
            - dl * dl1 * (81.70 + 9.412 * dl1)
        )
        * y1
    )
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c3ns3b(y, args):
    nf = args[0]
    dl1 = np.log(1.0 - y)
    dm = 1.0 / (1.0 - y)
    res = (
        +1536.0 * d81 * dl1**5
        - 16320.0 * d81 * dl1**4
        + 5.01099e2 * dl1**3
        + 1.17154e3 * dl1**2
        - 7.32845e3 * dl1
        + 4.44276e3
        + nf
        * (
            640.0 * d81 * dl1**4
            - 6592.0 * d81 * dl1**3
            + 220.573 * dl1**2
            + 294.906 * dl1
            - 729.359
        )
        + nf**2
        * (64.0 * d81 * dl1**3 - 464.0 * d81 * dl1**2 + 7.67505 * dl1 + 1.00830)
    )
    res = dm * res
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c3nm3c(y, args):
    nf = args[0]
    dl1 = np.log(1.0 - y)
    res = (
        +256.0 * d81 * dl1**6
        - 3264.0 * d81 * dl1**5
        + 1.252745e2 * dl1**4
        + 3.905133e2 * dl1**3
        - 3.664225e3 * dl1**2
        + 4.44276e3 * dl1
        - 9195.48
        + 22.80
        + nf
        * (
            128.0 * d81 * dl1**5
            - 1648.0 * d81 * dl1**4
            + 220.573 * d3 * dl1**3
            + 147.453 * dl1**2
            - 729.359 * dl1
            + 2575.074
            + 0.386
        )
        + nf**2
        * (
            16.0 * d81 * dl1**4
            - 464.0 * d81 * d3 * dl1**3
            + 7.67505 * 1 / 5.0 * dl1**2
            + 1.0083 * dl1
            - 103.2521
            - 0.0081
        )
    )
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c3np3a(y, args):
    return c3nm3a(y, args) + c3q3dfp(y, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def c3np3c(y, args):
    return c3nm3c(y, args) + c3q3dfpc(y, args)
