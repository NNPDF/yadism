# -*- coding: utf-8 -*-
# auto-generated module by light package
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def cls2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = nf * ( (15.94 - 5.212 * y) * (1.-y)**2 * dl1 + (0.421 + 1.520 * y) * dl**2 + 28.09 * (1.-y) * dl - (2.370/y - 19.27) * (1.-y)**3 )
    return res

@nb.njit("f8(f8,f8[:])", cache=True)
def clg2a(y, args):
    nf = args[0]
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = nf * ( (94.74 - 49.20 * y) * (1.-y) * dl1**2 + 864.8 * (1.-y) * dl1 + 1161.* y * dl * dl1 + 60.06 * y * dl**2 + 39.66 * (1.-y) * dl - 5.333 * (1./y - 1.) )
    return res
