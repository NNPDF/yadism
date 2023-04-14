"""Note, the factor `fl11` is disabled for charged currents according to `xcdiff3p.f`.
To generate `clnm3a,clnm3c` we follow `xcdiff3p.f` or the reference paper :cite:`Davies:2016ruz`
"""
import numba as nb
import numpy as np

from ...special.nielsen import nielsen
from ...special.zeta import zeta2
from .common import d81
from .xcdiff3p import clq3dfp


@nb.njit("f8(f8,f8[:])", cache=True)
def clnp3a(y, args):
    nf = args[0]
    fl11 = args[1]
    dl = np.log(y)
    dl1 = np.log(1.0 - y)
    li2 = nielsen(1, 1, y).real
    res = (
        -2220.5
        - 7884.0 * y
        + 4168.0 * y**2
        - 1280.0 * d81 * dl**3
        - 7456.0 / 27.0 * dl**2
        - 1355.7 * dl
        + 512.0 / 27 * dl1**4
        - 177.40 * dl1**3
        + 650.6 * dl1**2
        - 2729.0 * dl1
        + 208.3 * y * dl**3
        - dl1**3 * (1.0 - y) * (125.3 - 195.6 * dl1)
        - dl * dl1 * (844.7 * dl + 517.3 * dl1)
        + nf
        * (
            408.4
            - 9.345 * y
            - 919.3 * y**2
            + 1728.0 * d81 * dl**2
            + 200.73 * dl
            - 1792.0 * d81 * y * dl**3
            + 1024.0 * d81 * dl1**3
            - 112.35 * dl1**2
            + 344.1 * dl1
            + (1.0 - y) * dl1**2 * (239.7 + 20.63 * dl1)
            + dl * dl1 * (887.3 + 294.5 * dl - 59.14 * dl1)
        )
        + nf**2
        * (
            -19.0
            + (317.0 / 6.0 - 12.0 * zeta2) * y
            + 9.0 * y * dl**2
            + dl * (-6.0 + 50.0 * y)
            + 3.0 * y * dl1**2
            + dl1 * (6.0 - 25.0 * y)
            - 6.0 * y * dl * dl1
            + 6.0 * y * li2
        )
        * 64.0
        * d81
        + fl11
        * nf
        * (
            (107.0 + 321.05 * y - 54.62 * y**2) * (1.0 - y)
            - 26.717
            - 320 * d81 * dl**3
            - 640.0 * d81 * dl**2
            + 9.773 * dl
            + y * dl * (363.8 + 68.32 * dl)
        )
        * y
    )
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def clnp3c(y, args):
    nf = args[0]
    res = 0.113 + nf * 0.006
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def clnm3a(y, args):
    return clnp3a(y, args) - clq3dfp(y, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def clnm3c(y, args):
    return clnp3c(y, args)
