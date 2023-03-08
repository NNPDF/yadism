import numba as nb
import numpy as np
from eko.constants import CF, TR

from . import f2


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, _args):
    return (
        2
        * CF
        * (
            -(1 + z) * np.log(1 - z)
            - (1 + z**2) * np.log(z) / (1 - z)
            + 3.0
            + 2.0 * z
        )
    )


# The coefficients are the same as
# F2LIGHT_NS
ns_delta = f2.ns_delta
ns_omx = f2.ns_omx
ns_logomx = f2.ns_logomx
