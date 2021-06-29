import numba as nb
from eko.constants import CF

from . import f2


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, args):
    return f2.ns_reg(z, args) - 2 * CF * (1 + z)
