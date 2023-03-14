import numba as nb

from . import f2


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, _args):
    return f2.ns_reg(z, _args)


# The coefficients are the same as
# F2LIGHT_NS
ns_delta = f2.ns_delta
ns_omx = f2.ns_omx
ns_logomx = f2.ns_logomx
