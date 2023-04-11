# auto-generated module by light package
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def c2s2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res =   nf * ( 5.290 * (1./y-1.) + 4.310 * dl**3 - 2.086 * dl**2 + 39.78 * dl - 0.101 * (1.-y) * dl1**3 - (24.75 - 13.80 * y) * dl**2 * dl1 + 30.23 * dl * dl1 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2g2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res =   nf * ( 1./y * (11.90 + 1494.* dl1) + 5.319 * dl**3 - 59.48 * dl**2 - 284.8 * dl + 392.4 - 1483.* dl1 + (6.445 + 209.4 * (1.-y)) * dl1**3 - 24.00 * dl1**2 - 724.1 * dl**2 * dl1 - 871.8 * dl * dl1**2 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2g2c(y, args):
    nf = args[0]
    res = - nf * 0.28
    return res
