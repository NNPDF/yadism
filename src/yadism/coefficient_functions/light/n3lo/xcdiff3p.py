"""Difference even N - odd N moments"""
import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def c2q3dfp(y, args):
    nf = args[0]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(y1)
    c2q30 = (
        273.59
        - 44.95 * y
        - 73.56 * y**2
        + 40.68 * y**3
        + 0.1356 * dl**5
        + 8.483 * dl**4
        + 55.90 * dl**3
        + 120.67 * dl**2
        + 388.0 * dl
        - 329.8 * dl * dl1
        - y * dl * (316.2 + 71.63 * dl)
        + 46.30 * dl1
        + 5.447 * dl1**2
    )
    c2q31 = (
        -19.093
        + 12.97 * y
        + 36.44 * y**2
        - 29.256 * y**3
        - 0.76 * dl**4
        - 5.317 * dl**3
        - 19.82 * dl**2
        - 38.958 * dl
        - 13.395 * dl * dl1
        + y * dl * (14.44 + 17.74 * dl)
        + 1.395 * dl1
    )
    res = (c2q30 + nf * c2q31) * y1
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2q3dfpc(y, args):
    nf = args[0]
    res = -0.0008 + 0.0001 * nf
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def clq3dfp(y, args):
    nf = args[0]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(y1)
    clq30 = (
        -620.53
        - 394.5 * y
        + 1609.0 * y**2
        - 596.2 * y**3
        + 0.217 * dl**3
        + 62.18 * dl**2
        + 208.47 * dl
        - 482.5 * dl * dl1
        - y * dl * (1751.0 - 197.5 * dl)
        + 105.5 * dl1
        + 0.442 * dl1**2
    )
    clq31 = (
        -6.500
        - 12.435 * y
        + 23.66 * y**2
        + 0.914 * y**3
        + 0.015 * dl**3
        - 6.627 * dl**2
        - 31.91 * dl
        - y * dl * (5.711 + 28.635 * dl)
    )
    res = (clq30 + nf * clq31) * y1**2
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c3q3dfp(y, args):
    nf = args[0]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(y1)
    c3q30 = (
        -553.5
        + 1412.5 * y
        - 990.3 * y**2
        + 361.1 * y**3
        + 0.1458 * dl**5
        + 9.688 * dl**4
        + 90.62 * dl**3
        + 83.684 * dl**2
        - 602.32 * dl
        - 382.5 * dl * dl1
        - y * dl * (2.805 + 325.92 * dl)
        + 133.5 * dl1
        + 10.135 * dl1**2
    )
    c3q31 = (
        -16.777
        + 77.78 * y
        - 24.81 * y**2
        - 28.89 * y**3
        - 0.7714 * dl**4
        - 7.701 * dl**3
        - 21.522 * dl**2
        - 7.897 * dl
        - 16.17 * dl * dl1
        + y * dl * (43.21 + 67.04 * dl)
        + 1.519 * dl1
    )
    res = (c3q30 + nf * c3q31) * y1
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c3q3dfpc(y, args):
    nf = args[0]
    res = -0.0029 + 0.00006 * nf
    return res
