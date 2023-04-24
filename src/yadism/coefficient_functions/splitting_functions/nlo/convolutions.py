# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np
from eko.constants import CA, CF, TR

from ...special import li2


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0_2_reg(z, _args):
    return -4*CF**2*(5 + z + 4*(1 + z)*np.log(1 - z) - 3*(1 + z)*np.log(z))

@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0_2_sing(z, _args):
    return (-8*CF**2*(3 + 4*np.log(1 - z) - 2*np.log(z)))/(-1 + z)

@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0_2_loc(z, _args):
    return (CF**2*(27 + 8*np.pi**2 + 12*(3 - 4*np.log(1 - z))*np.log(1 - z) - 48*li2(1 - z)))/3.

@nb.njit("f8(f8,f8[:])", cache=True)
def pqq0pqg0_reg(z,args):
    nf = args[0]
    return 4*CF*nf*TR*(-1 + 4*z + (4 + 8*(-1 + z)*z)*np.log(1 - z) + (-2 + 4*z - 8*z**2)*np.log(z))

@nb.njit("f8(f8,f8[:])", cache=True)
def pqg0pgg0_reg(z,args):
    nf = args[0]
    return (4*nf*TR*(-2*nf*z*(1 + 2*(-1 + z)*z) + CA*(8 + z*(17 + 26*z - 40*z**2)) + 12*CA*(z*(1 + 2*(-1 + z)*z)*np.log(1 - z) + z*(1 + 4*z)*np.log(z))))/(3.*z)

@nb.njit("f8(f8,f8[:])", cache=True)
def pqg0pgq0_reg(z,args):
    nf = args[0]
    return 8*CF*nf*TR*(1 + 4/(3.*z) - z - (4*z**2)/3. + 2*(1 + z)*np.log(z))
