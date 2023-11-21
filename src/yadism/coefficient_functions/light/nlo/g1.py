import numba as nb
import numpy as np
from eko.constants import TR

from . import f2, f3


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, args):
    return f3.ns_reg(z, args)


# The coefficients are the same as
# F2LIGHT_NS
ns_delta = f2.ns_delta
ns_omx = f2.ns_omx
ns_logomx = f2.ns_logomx


@nb.njit("f8(f8,f8[:])", cache=True)
def gluon_reg(z, args):
    nf = args[0]
    return 4.0 * nf * TR * ((2.0 * z - 1.0) * np.log((1.0 - z) / z) - 4.0 * z + 3.0)
