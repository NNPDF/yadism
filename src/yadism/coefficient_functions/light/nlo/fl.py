import numba as nb
import numpy as np
from eko.constants import CF, TR


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, args):
    return CF * 4.0 * z


@nb.njit("f8(f8,f8[:])", cache=True)
def gluon_reg(z, args):
    nf = args[0]
    return nf * TR * 16 * z * (1.0 - z)
