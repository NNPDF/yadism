"""Note, the factor `fl11` is disabled for charged currents according to `xcdiff3p.f`.
To generate `c2nm3a,c2nm3c` we follow `xcdiff3p.f` or the reference paper :cite:`Davies:2016ruz`.
"""
import numba as nb
import numpy as np

from .common import d3, d27, d81, d243
from .xcdiff3p import c2q3dfp, c2q3dfpc


@nb.njit("f8(f8,f8[:])", cache=True)
def c2np3a(y, args):
    nf = args[0]
    fl11 = args[1]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(1.0 - y)
    res = (
        -4926.0
        + 7725.0 * y
        + 57256.0 * y**2
        + 12898.0 * y**3
        - 32.0 * d27 * dl**5
        - 8796.0 * d243 * dl**4
        - 309.1 * dl**3
        - 899.6 * dl**2
        - 775.8 * dl
        + 4.719 * y * dl**5
        - 512.0 * d27 * dl1**5
        + 6336.0 * d27 * dl1**4
        - 3368.0 * dl1**3
        - 2978.0 * dl1**2
        + 18832.0 * dl1
        - 56000.0 * (1.0 - y) * dl1**2
        - dl * dl1 * (6158.0 + 1836.0 * dl)
        + nf
        * (
            831.6
            - 6752.0 * y
            - 2778.0 * y**2
            + 728.0 * d243 * dl**4
            + 12224.0 * d243 * dl**3
            + 187.3 * dl**2
            + 275.6 * dl
            + 4.102 * y * dl**4
            - 1920.0 * d243 * dl1**4
            + 153.5 * dl1**3
            - 828.7 * dl1**2
            - 501.1 * dl1
            + 171.0 * (1.0 - y) * dl1**4
            + dl * dl1 * (4365.0 + 716.2 * dl - 5983.0 * dl1)
        )
        + nf**2
        * (
            129.2 * y
            + 102.5 * y**2
            - 368.0 * d243 * dl**3
            - 1984.0 * d243 * dl**2
            - 8.042 * dl
            - 192.0 * d243 * dl1**3
            + 18.21 * dl1**2
            - 19.09 * dl1
            + dl * dl1 * (-96.07 - 12.46 * dl + 85.88 * dl1)
        )
        + fl11
        * nf
        * (
            (126.42 - 50.29 * y - 50.15 * y**2) * y1
            - 26.717
            - 960.0 * d243 * dl**2 * (dl + 5.0)
            + 59.59 * dl
            - y * dl**2 * (101.8 + 34.79 * dl + 3.070 * dl**2)
            - 9.075 * y * y1 * dl1
        )
        * y
    )
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns3b(y, args):
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
def c2np3c(y, args):
    nf = args[0]
    fl11 = args[1]
    dl1 = np.log(1.0 - y)
    res = (
        +256.0 * d81 * dl1**6
        - 3264.0 * d81 * dl1**5
        + 1.252745e2 * dl1**4
        + 3.905133e2 * dl1**3
        - 3.664225e3 * dl1**2
        + 4.44276e3 * dl1
        - 9195.48
        + 25.10
        + nf
        * (
            128.0 * d81 * dl1**5
            - 1648.0 * d81 * dl1**4
            + 220.573 * d3 * dl1**3
            + 147.453 * dl1**2
            - 729.359 * dl1
            + 2575.074
            - 0.387
        )
        + nf**2
        * (
            16.0 * d81 * dl1**4
            - 464.0 * d81 * d3 * dl1**3
            + 7.67505 * 1 / 5.0 * dl1**2
            + 1.0083 * dl1
            - 103.2521
            + 0.0155
        )
        - fl11 * nf * 11.8880
    )
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2nm3a(y, args):
    return c2np3a(y, args) - c2q3dfp(y, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def c2nm3c(y, args):
    return c2np3c(y, args) - c2q3dfpc(y, args)
