import numba as nb
from eko.constants import CF


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, _args):
    return 4 * CF * z
