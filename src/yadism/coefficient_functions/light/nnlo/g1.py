"""|NNLO| g1 expressions taken from https://github.com/vbertone/apfelxx/blob/master/src/structurefunctions/zeromasscoefficientfunctionspol_sl.cc"""
import numba as nb
import numpy as np
from eko.constants import CA, CF, TR

from ...special import li2, zeta2, zeta3
from ...special.nielsen import nielsen


@nb.njit("f8(f8,f8[:])", cache=True)
def singlet_reg(z, args):
    nf = args[0]
    z2 = z**2
    Li31mz = nielsen(2, 1, 1 - z).real
    Li21mz = li2(1 - z)
    Li2mz = li2(-z)
    ln1mz = np.log(1 - z)
    ln1mz2 = ln1mz**2
    lnz = np.log(z)
    lnz2 = lnz**2
    lnz3 = lnz**3
    ln1pz = np.log(1 + z)

    return (
        nf
        * CF
        * TR
        * (
            (1 + z)
            * (
                -16 * Li31mz
                + 16 * ln1mz * Li21mz
                - 16 * lnz * Li21mz
                - 16 * zeta2 * lnz
                + 8 * lnz * ln1mz2
                - 16 * lnz2 * ln1mz * 20 * lnz3 / 3.0
            )
            + (1 - z) * (20 * ln1mz2 - 88 * ln1mz + 760 / 3)
            - 32 * (1 + z2 / 3.0 + z + 1 / z / 3.0) * (Li2mz + lnz * ln1pz)
            + (50 + 16 * z2 / 3.0 - 10 * z) * lnz2
            - 32 * (2 - z) * lnz * ln1mz
            + 4 * (119 - 13 * z) * lnz / 3.0
            - (72 + 32 * z2 / 3.0 - 40 * z) * zeta2
            - 8 * (3 + z) * Li21mz
        )
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def gluon_reg(z, args):
    nf = args[0]
    z2 = z**2
    S121mz = nielsen(1, 2, 1 - z).real
    S12mz = nielsen(1, 2, -z).real
    Li31mz = nielsen(2, 1, 1 - z).real
    Li3mz = nielsen(2, 1, -z).real
    Li3r = nielsen(2, 1, (1 - z) / (1 + z)).real
    Li3mr = nielsen(2, 1, -(1 - z) / (1 + z)).real
    Li21mz = li2(1 - z)
    Li2mz = li2(-z)
    ln1mz = np.log(1 - z)
    ln1mz2 = ln1mz * ln1mz
    ln1mz3 = ln1mz * ln1mz2
    lnz = np.log(z)
    lnz2 = lnz**2
    lnz3 = lnz**3
    ln1pz = np.log(1 + z)
    ln1pz2 = ln1pz**2

    return nf * (
        CF
        * TR
        * (
            (1 - 2 * z)
            * (
                32 * Li31mz
                - 16 * ln1mz * Li21mz
                - 8 * lnz * Li21mz
                - 24 * zeta2 * lnz
                - 20 * ln1mz3 / 3.0
                + 16 * lnz * ln1mz2
                - 16 * lnz2 * ln1mz
                + 10 * lnz3 / 3
            )
            - 16
            * (1 + z2 + 2 * z)
            * (
                4 * S12mz
                + 4 * ln1pz * Li2mz
                + 2 * lnz * ln1pz2
                - lnz2 * ln1pz
                + 2 * zeta2 * ln1pz
            )
            - 32 * (1 + z2 - 6 * z) * Li3mz
            + 8 * (1 + 4 * z2 - 2 * z) * S121mz
            + 16 * (13 * z2 + 12 * z + 4.0 / z) * (Li2mz + lnz * ln1pz) / 3.0
            + 4 * (5 - 12 * z) * Li21mz
            + 32 * (1 + z2 - 2 * z) * lnz * Li2mz
            + (123 - 104 * z2 - 48 * z) * lnz2 / 3.0
            - (88 - 96 * z) * lnz * ln1mz
            + 6 * (9 - 12 * z) * ln1mz2
            - 32 * zeta2 * z2 * ln1mz
            - 4 * (31 - 4 * z2 - 26 * z) * ln1mz
            + (416 - 48 * z2 - 274 * z) * lnz / 3.0
            - 8 * (5 - 4 * z2 - 26 * z) * zeta3
            - 4 * (81 - 52 * z2 - 108 * z) * zeta2 / 3.0
            + 2 * (233 - 239 * z) / 3.0
        )
        + CA
        * TR
        * (
            16
            * (1 + 2 * z)
            * (Li3r - Li3mr - ln1mz * Li2mz - lnz * Li21mz - lnz * ln1mz * ln1pz)
            + 16
            * (1 + z2 + 2 * z)
            * (2 * S12mz + lnz * ln1pz2 + 2 * ln1pz * Li2mz + zeta2 * ln1pz)
            + 8 * (1 - 2 * z2 + 2 * z) * S121mz
            - 8 * (9 + 2 * z) * Li31mz
            - 8 * (1 - z2 + 2 * z) * (2 * Li3mz - lnz2 * ln1pz - 2 * lnz * Li2mz)
            - 16 * (2 + z) * lnz2 * ln1mz
            + 24 * (lnz * ln1mz2 - 2 * zeta2 * lnz - Li21mz)
            - 16 * (6 + 11 * z2 + 12 * z + 2.0 / z) * (Li2mz + lnz * ln1pz) / 3.0
            - 4 * (1 - 2 * z) * ln1mz3 / 3.0
            + 8 * (6 - 7 * z) * ln1mz2
            + 8 * (3 + 2 * z2 - 10 * z) * zeta2 * ln1mz
            + 4 * (7 + 10 * z) * lnz3 / 3.0
            + 2 * (135 + 44 * z2 - 48 * z) * lnz2 / 3.0
            - 8 * (17 - 16 * z) * lnz * ln1mz
            + 8 * (118 + 3 * z2 - 26 * z) * lnz / 3.0
            - 4 * (44 + 2 * z2 - 53 * z) * ln1mz
            - 4 * (3 + 4 * z2 + 10 * z) * zeta3
            - 16 * (27 + 11 * z2 - 24 * z) * zeta2 / 3.0
            + 8 * (5 + 2 * z) * ln1mz * Li21mz
            + 4 * (355 - 367 * z) / 3.0
        )
        + CF
        * TR
        * (
            16 * (1 + 2 * z) * (2 * Li21mz + 2 * lnz * ln1mz - lnz2)
            + 96 * (1 - z) * ln1mz
            - (144 + 64 * z) * lnz
            - 304 * (1 - z)
        )
    )
