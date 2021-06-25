# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np
from eko.constants import CA, CF, TR


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0_2_reg(z, _args):
    return -4*CF**2*(5 + z + 4*(1 + z)*np.log(1 - z) - 3*(1 + z)*np.log(z))

pqq0_2_coeffs = ((CF**2*(27 - 8*np.pi**2))/3.,24*CF**2,32*CF**2)

@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0pqg0_reg(z,args):
    nf = args[0]
    return 4*CF*nf*TR*(-1 + 4*z + (4 + 8*(-1 + z)*z)*np.log(1 - z) + (-2 + 4*z - 8*z**2)*np.log(z))

@nb.njit("f8(f8,f8[:])", cache=True)
def pqg0pgg0_reg(z,args):
    nf = args[0]
    return (4*nf*TR*(-2*nf*z*(1 + 2*(-1 + z)*z) + CA*(8 + z*(26 - z*(10 + 13*z))) + 3*CA*z*((1 + 2*(-1 + z)*z)*np.log(1 - z) + (7 + 2*z*(5 + 3*z))*np.log(z))))/(3.*z)

@nb.njit("f8(f8,f8[:])", cache=True)
def pqg0pgq0_reg(z,args):
    nf = args[0]
    return 8*CF*nf*TR*(1 + 4/(3.*z) - z - (4*z**2)/3. + 2*(1 + z)*np.log(z))
