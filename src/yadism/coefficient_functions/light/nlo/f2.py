import numba as nb
import numpy as np
from eko.constants import CF, TR

zeta_2 = np.pi**2 / 6.0


@nb.njit("f8(f8,f8[:])", cache=True)
def ns_reg(z, args):
    # fmt: off
    return CF*(
        - 2 * (1 + z) * np.log((1 - z) / z)
        - 4 * np.log(z) / (1 - z)
        + 6 + 4 * z
    )
    # fmt: on


ns_delta = -CF * (9 + 4 * zeta_2)
ns_omx = -3 * CF
ns_logomx = 4 * CF


@nb.njit("f8(f8,f8[:])", cache=True)
def gluon_reg(z, args):
    nf = args[0]
    return (
        nf
        * (
            (2.0 - 4.0 * z * (1.0 - z)) * np.log((1.0 - z) / z)
            - 2.0
            + 16.0 * z * (1.0 - z)
        )
        * (2.0 * TR)
    )
