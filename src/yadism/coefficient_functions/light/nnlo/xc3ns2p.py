# -*- coding: utf-8 -*-
# auto-generated module by light package
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def c3nm2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = - 206.1 - 576.8 * y - 3.922 * dl**3 - 33.31 * dl**2 - 67.60 * dl - 15.20 * dl1**3 + 94.61 * dl1**2 - 409.6 * dl1 - 147.9 * dl * dl1**2 + nf * ( - 6.337 - 14.97 * y + 2.207 * dl**2 + 8.683 * dl + 0.042 * dl1**3 - 0.808 * dl1**2 + 25.00 * dl1 + 9.684 * dl * dl1 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c3np2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = - 242.9 - 467.2 * y - 3.049 * dl**3 - 30.14 * dl**2 - 79.14 * dl - 15.20 * dl1**3 + 94.61 * dl1**2 - 396.1 * dl1 - 92.43 * dl * dl1**2 + nf * ( - 6.337 - 14.97 * y + 2.207 * dl**2 + 8.683 * dl + 0.042 * dl1**3 - 0.808 * dl1**2  + 25.00 * dl1 + 9.684 * dl * dl1 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c3ns2b(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    dm  = 1./(1.-y)
    res = + 14.2222 * dl1**3 - 61.3333 * dl1**2 - 31.105 * dl1 + 188.64 + nf * ( 1.77778 * dl1**2 - 8.5926 * dl1 + 6.3489 )
    res = dm * res
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c3nm2c(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    res = + 3.55555 * dl1**4 - 20.4444 * dl1**3 - 15.5525 * dl1**2 + 188.64 * dl1 - 338.531 - 0.104 + nf * (0.592593 * dl1**3 - 4.2963 * dl1**2 + 6.3489 * dl1 + 46.844 + 0.013)
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def c3np2c(y, args):
    nf = args[0]
    dl1 = np.log(1.-y)
    res = + 3.55555 * dl1**4 - 20.4444 * dl1**3 - 15.5525 * dl1**2 + 188.64 * dl1 - 338.531  - 0.152 + nf * (0.592593 * dl1**3 - 4.2963 * dl1**2 + 6.3489 * dl1 + 46.844 + 0.013)
    return res
