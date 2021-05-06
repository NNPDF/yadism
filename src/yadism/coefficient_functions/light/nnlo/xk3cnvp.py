# -*- coding: utf-8 -*-
# fmt: off
import numpy as np


def c2q1sa (y):
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    return (- 410.5 - 483.3 * y- 1.230 * dl**3 + 9.466 * dl**2 + 32.45 * dl- 26.51 * dl1**3 + 192.9 * dl1**2 + 198.2 * dl1+ 113.0 * dl * dl1**2)

def c3q1sa (y):
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    return (- 335.7 - 305.3* y- 1.198 * dl**3 + 3.054 * dl**2 + 65.54 * dl- 27.09 * dl1**3 + 162.1 * dl1**2 + 248.0 * dl1+ 91.79 * dl * dl1**2)

def c2q1sb (y):
    dl1 = np.log(1.-y)
    dm  = 1./(1.-y)
    return (+ 28.4444 * dl1**3 - 64.d0 * dl1**2 - 283.157 * dl1+ 304.751)
    return ( dm * c2q1sb)

def c2q1sc (y):
    dl1 = np.log(1.-y)
    return (+ 7.1111 * dl1**4 - 21.3333 * dl1**3 - 141.579 * dl1**2+ 304.751 * dl1 + 346.213)

def c3q1sc (y):
    dl1 = np.log(1.-y)
    return (+ 7.1111 * dl1**4 - 21.3333 * dl1**3 - 141.579 * dl1**2+ 304.751 * dl1 + 345.993)