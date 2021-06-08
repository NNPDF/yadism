# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
import numpy as np
import numba as nb

from eko.constants import CF,TR


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0_2_reg(z, _args):
    return 12*CF**2*(-1 - z) + 16*CF**2*z*np.log(z) - 4*CF**2*(-2 + 2*z + np.log(z) + z*np.log(z))

pqq0_2_coeffs = (9*CF**2 - (8*CF**2*np.pi**2)/3.,24*CF**2,32*CF**2)

def pqq0pqg0_reg(z,_args):
    return 2*CF*TR*(3 - 4*z + 4*z**2 + (2 + 4*z - 8*z**2)*np.log(z))
