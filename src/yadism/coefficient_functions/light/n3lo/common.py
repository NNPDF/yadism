# -*- coding: utf-8 -*-
"""common factors see :cite:`vogt-f2nc` table 2"""
import numba as nb

d3 = 1 / 3.0
d9 = 1 / 9.0
d27 = 1.0 / 27.0
d81 = 1.0 / 81.0
d243 = 1.0 / 243.0


@nb.njit("f8(i4)", cache=True)
def fl(nf):
    fl = [2.0, 0.5, 0.0, 0.5, 0.2, 0.5]
    return fl[int(nf-1)]


@nb.njit("f8(i4)", cache=True)
def fls(nf):
    fls = [1.0, 0.1, 0.0, 0.1, 0.01818181818, 0.1]
    return fls[int(nf-1)]


@nb.njit("f8(i4)", cache=True)
def flg(nf):
    return fls(nf)
