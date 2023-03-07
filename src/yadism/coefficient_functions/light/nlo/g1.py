import numba as nb
import numpy as np
from eko.constants import TR, CF

from . import f2


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(x, args):
    return (
        2
        * CF
        * (-(1 + x) * np.log(1 - x) - (1 + x**2) * np.log(x) / (1 - x) + 2.0 + x)
    )


# The coefficients are the same as
# F2LIGHT_NS
ns_delta = f2.ns_delta
ns_omx = f2.ns_omx
ns_logomx = f2.ns_logomx


@nb.njit("f8(f8,f8[:])", cache=True)
def gluon_reg(z, args):
    nf = args[0]
    return 4.0 * nf * TR * ((2.0 * z - 1.0) * np.log((1.0 - z) / z) - 4.0 * z + 3.0)
