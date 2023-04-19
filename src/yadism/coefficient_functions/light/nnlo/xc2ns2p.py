# auto-generated module by light package
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def c2nn2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = - 69.59 - 1008.* y - 2.835 * dl**3 - 17.08 * dl**2 + 5.986 * dl - 17.19 * dl1**3 + 71.08 * dl1**2 - 660.7 * dl1 - 174.8 * dl * dl1**2 + 95.09 * dl**2 * dl1 + nf * ( - 5.691 - 37.91 * y + 2.244 * dl**2 + 5.770 * dl - 1.707 * dl1**2  + 22.95 * dl1 + 3.036 * dl**2 * dl1 + 17.97 * dl * dl1 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2nc2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = - 84.18 - 1010.* y - 3.748 * dl**3 - 19.56 * dl**2 - 1.235 * dl - 17.19 * dl1**3 + 71.08 * dl1**2 - 663.0 * dl1 - 192.4 * dl * dl1**2 + 80.41 * dl**2 * dl1 + nf * ( - 5.691 - 37.91 * y + 2.244 * dl**2 + 5.770 * dl - 1.707 * dl1**2  + 22.95 * dl1 + 3.036 * dl**2 * dl1 + 17.97 * dl * dl1 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns2b(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    dm  = 1./(1.-y)
    res = + 14.2222 * dl1**3 - 61.3333 * dl1**2 - 31.105 * dl1 + 188.64 + nf * ( 1.77778 * dl1**2 - 8.5926 * dl1 + 6.3489 )
    res = dm * res
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2nn2c(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    res = + 3.55555 * dl1**4 - 20.4444 * dl1**3 - 15.5525 * dl1**2 + 188.64 * dl1 - 338.531 + 0.485 + nf * (0.592593 * dl1**3 - 4.2963 * dl1**2 + 6.3489 * dl1 + 46.844 - 0.0035)
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c2nc2c(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    res = + 3.55555 * dl1**4 - 20.4444 * dl1**3 - 15.5525 * dl1**2 + 188.64 * dl1 - 338.531 + 0.537 + nf * (0.592593 * dl1**3 - 4.2963 * dl1**2 + 6.3489 * dl1 + 46.844 - 0.0035)
    return res
