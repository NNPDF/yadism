"""Polarized, asymptotic coefficient functions from :cite:`Bierenbaum:2022biv`."""
import numba as nb
import numpy as np

from ..special import li2, zeta2, zeta3
from ..special.nielsen import nielsen


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_LL_reg(z, args):
    """|ref| implements |LL| regular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return 2 / 3 * (-4 / 3 - 4 * z / 3) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_LL_loc(z, args):
    """|ref| implements |LL| local part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return (4 / 3 + 16 / 9 * np.log(1 - z)) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_LL_sing(z, args):
    """|ref| implements |LL| singular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return 16 / (9 * (1 - z)) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NLL_reg(z, args):
    """|ref| implements |NLL| regular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return (
        (2 / 3) * (8 / 9 - 88 * z / 9 - 8 * np.log(z) / 3 - 8 / 3 * z * np.log(z)) * L
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NLL_loc(z, args):
    """|ref| implements |NLL| local part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    Li2m1 = li2(1 / (1 - z))
    return L * (
        4 / 9
        - (16 / 27)
        * (
            np.pi**2
            + (-10 + 6 * 1j * np.pi) * np.log(1 - z)
            - 3 * np.log(1 - z) ** 2
            - 6 * Li2m1
        ).real
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NLL_sing(z, args):
    """|ref| implements |NLL| singular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return (2 / 3) * (+80 / 9 + 16 * np.log(z) / 3) / (1 - z) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NNLL_reg(z, _args):
    """|ref| implements |NNLL| regular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    Li2 = li2(z)
    return (2 / 3) * (
        -(188 / 27)
        - (104 * l) / 9
        - 4 * l2
        - (8 * Li2) / 3
        + (40 * lm) / 9
        + (8 * l * lm) / 3
        - (4 * lm2) / 3
        - (872 * z) / 27
        - (224 * l * z) / 9
        - 4 * l2 * z
        - (8 * Li2 * z) / 3
        + (112 * lm * z) / 9
        + (8 * l * lm * z) / 3
        - (4 * lm2 * z) / 3
        + (16 * zeta2) / 3
        + (16 * z * zeta2) / 3
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NNLL_loc(z, _args):
    """|ref| implements |NNLL| local part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    Li2 = li2(z)
    Li2m = li2(1 - z)
    Li2m1 = li2(1 / (1 - z))
    Li3 = nielsen(2, 1, z)
    Li3m = nielsen(2, 1, 1 - z)
    Li3m1 = nielsen(2, 1, 1 / (1 - z))
    return (
        530 / 27
        + 4
        / 81
        * (
            -67 * np.pi**2
            + 359 * lm
            - 402 * 1j * np.pi * lm
            - 144 * zeta2 * lm
            + 114 * lm2
            + 36 * 1j * np.pi * lm2
            - 12 * lm**3
            + 72 * lm2 * l
            + 108 * lm * l2
            + (402 - 72 * lm) * Li2m1
            + 144 * lm * Li2m
            + 72 * lm * Li2
            + 216 * l * Li2
            - 72 * Li3m1
            - 144 * Li3m
            - 216 * Li3
            + 216 * zeta3
        ).real
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ns_NNLL_sing(z, _args):
    """|ref| implements |NNLL| sigular part of :eqref:`254`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    Li2 = li2(z)
    return (
        (2 / 3)
        * (
            +718 / (27)
            + (268 * l) / (9)
            + (8 * l2)
            + (16 * Li2) / 3
            - (116 * lm) / 9
            - (16 * l * lm) / 3
            + (8 * lm2) / 3
            - (32 * zeta2) / 3
        )
        / (1 - z)
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ps_LL_reg(z, args):
    """|ref| implements |LL| part of :eqref:`261`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return 2 / 3 * (20 * (-1 + z) - 8 * (1 + z) * np.log(z)) * L**2


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ps_NLL_reg(z, args):
    """|ref| implements |NLL| part of :eqref:`261`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return (
        2
        / 3
        * (-8 * (-1 + z) + 8 * (-1 + 3 * z) * np.log(z) - 8 * (1 + z) * np.log(z) ** 2)
        * L
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2ps_NNLL_reg(z, _args):
    """|ref| implements |NNLL| part of :eqref:`261`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    lp = np.log(1 + z)
    Li2 = li2(z)
    mLi2 = li2(-z)
    Li3 = nielsen(2, 1, z).real
    Li3m = nielsen(2, 1, 1 - z).real
    return (8 / 27) * (
        -444 * (-1 + z)
        + 18 * (11 + 10 * l) * lm * (-1 + z)
        - 45 * lm2 * (-1 + z)
        + 12 * l**3 * (1 + z)
        + 6 * lm * (-6 * Li2 - 3 * l * lm + 6 * zeta2) * (1 + z)
        - (24 * l * lp * (1 + z) ** 3) / z
        - 24 * zeta2 * (9 + (-3 + z) * z)
        + 6 * l2 * (21 + 2 * z**2)
        + 36 * Li2 * (-1 + 3 * z + 2 * l * (1 + z))
        - 12 * l * (16 * (-2 + z) + 6 * zeta2 * (1 + z))
        - (24 * (1 + z) ** 3 * mLi2) / z
        - 36 * (1 + z) * Li3m
        - 72 * (1 + z) * Li3
        + 72 * (1 + z) * zeta3
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c1g_LL_reg(z, args):
    """|ref| implements |LL| part of :eqref:`29`, :cite:`Bierenbaum:2022biv`."""
    L = args[0]
    return 2 * (2 * z - 1) * L


@nb.njit("f8(f8,f8[:])", cache=True)
def c1g_NLL_reg(z, _args):
    """|ref| implements |NLL| part of :eqref:`29`, :cite:`Bierenbaum:2022biv`."""
    return 2 * ((3 - 4 * z) + (2 * z - 1) * np.log((1 - z) / z))


@nb.njit("f8(f8,f8[:])", cache=True)
def c2g_LL_reg(z, args):
    """|ref| implements |LL| part of :eqref:`273`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    lm = np.log(1 - z)
    L = args[0]
    return (
        -(4 / 3) * (50 - 52 * z + 5 * lm * (-1 + 2 * z) + 2 * l * (8 + 11 * z)) * L**2
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2g_NLL_reg(z, args):
    """|ref| implements |NLL| part of :eqref:`273`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    lp = np.log(1 + z)
    Li2 = li2(z)
    mLi2 = li2(-z)
    L = args[0]
    return (
        -(4 / 3)
        * (
            -71
            - 4 * Li2
            + lm
            - lm2
            + 18 * mLi2
            + 69 * z
            + 8 * Li2 * z
            + 6 * lm * z
            + 2 * lm2 * z
            + 36 * mLi2 * z
            + l2 * (13 + 10 * z)
            + 2 * l * (8 + 9 * lp - 45 * z + 18 * lp * z + 8 * lm * (-1 + 2 * z))
            + 6 * zeta2
            + 24 * z * zeta2
        )
        * L
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def c2g_NNLL_reg(z, _args):
    """|ref| implements |NNLL| part of :eqref:`273`, :cite:`Bierenbaum:2022biv`."""
    l = np.log(z)
    l2 = l**2
    lm = np.log(1 - z)
    lm2 = lm**2
    lp = np.log(1 + z)
    lp2 = lp**2
    Li2 = li2(z)
    mLi2 = li2(-z)
    Li2m = li2(1 - z)
    Li2p = li2(1 + z)
    Li2pm = li2((1 + z) / (1 - z))
    Li3 = nielsen(2, 1, z)
    mLi3 = nielsen(2, 1, -z)
    Li3m = nielsen(2, 1, 1 - z)
    Li3p = nielsen(2, 1, 1 + z)
    Li3pm = nielsen(2, 1, (1 + z) / (1 - z))
    log2 = np.log(2)
    result = (
        (
            4436
            - 1164 * Li3
            - 720 * Li3m
            + 168 * Li3p
            + 216 * Li3pm
            - 3450 * lm
            + 909 * lm2
            + 6 * l2 * (225 - 27 * lm + 43 * lp)
            - 6
            * (
                Li2 * (75 + 64 * lm - 36 * lp)
                + 4
                * (
                    -9 * Li2m * lm
                    - 9 * Li2pm * lm
                    + 2 * np.power(lm, 3)
                    + 7 * Li2p * lp
                    + 9 * Li2pm * lp
                )
            )
        )
        + 4 * np.power(l, 3) * (31 + 28 * z)
        + 8
        * mLi2
        / z
        * (-2 + z * (-27 - z * (33 + 47 * z) + 6 * lp * (-8 + (-16 + z) * z)))
        + (
            complex(0, -12) * (9 * lm2 - 18 * lm * lp + 16 * lp2) * np.pi
            - 8
            * (
                553
                + 60 * l2
                - 189 * Li2
                + 87 * Li3
                + 90 * Li3m
                - 42 * Li3p
                - 54 * Li3pm
            )
            * z
            + 6
            * (
                (641 + 54 * l2 - 88 * Li2 + 72 * Li2m + 72 * Li2pm) * lm
                + 16 * np.power(lm, 3)
                - 188 * lm2
                + 86 * l2 * lp
                + 8 * (9 * Li2 - 7 * Li2p - 9 * Li2pm) * lp
            )
            * z
            + complex(0, 432) * lm * lp * np.pi * z
            - complex(0, 384) * lp2 * np.pi * z
            + 185 * l2 * np.power(z, 2)
            + 12 * Li2 * np.power(z, 2)
            + 24 * Li3 * np.power(z, 2)
            - 48 * Li3p * np.power(z, 2)
            - 12 * lm * np.power(z, 2)
            - 12 * l2 * lm * np.power(z, 2)
            - 12 * l2 * lp * np.power(z, 2)
            + 48 * Li2p * lp * np.power(z, 2)
            + complex(0, 24) * lp2 * np.pi * np.power(z, 2)
            + 3 * lm2 * z * (complex(0, -72) * np.pi + z)
            + 12 * mLi3 * (-43 + 2 * z * (21 + z))
            - 3012 * zeta2
            + 816 * lm * zeta2
            - 408 * lp * zeta2
            + 2184 * z * zeta2
            - 336 * lm * z * zeta2
            - 816 * lp * z * zeta2
            - 382 * np.power(z, 2) * zeta2
            + 24 * lm * np.power(z, 2) * zeta2
            + 24 * lp * np.power(z, 2) * zeta2
            - 216 * (1 + 2 * z) * (Li2p + complex(0, 1) * lp * np.pi - zeta2) * log2
        )
        - (2 * l)
        * (
            (
                -2114
                + 192 * lp2
                - 366 * mLi2
                + 1891 * z
                + 156 * lm2 * (-1 + 2 * z)
                + 18 * np.power(lm, 2) * (7 + 4 * z)
                + 6 * Li2 * (-79 + 2 * (-29 + z) * z)
                - 3 * lm * (-541 + z * (616 + z))
                - 6
                * z
                * (58 * mLi2 + 4 * lp2 * (-16 + z) + z - 2 * mLi2 * z - 4 * zeta2)
                + 528 * zeta2
            )
            + (4 * lp)
            / z
            * (
                2
                + z
                * (
                    -27 * lm * (1 + 2 * z)
                    + 27 * (1 + log2)
                    + z * (33 + 47 * z + 54 * log2)
                )
            )
        )
        - 216 * (1 + 2 * z) * (mLi2 * np.log(2 * z))
        + 6
        * (
            -36 * (lm - lp) * (1 + 2 * z) * li2((1 + z) / (-1 + z))
            - 36 * (1 + 2 * z) * nielsen(2, 1, -(1 + z) / (1 - z))
            + 5 * (11 + 46 * z) * zeta3
        )
    ) / (9.0)
    return result.real
