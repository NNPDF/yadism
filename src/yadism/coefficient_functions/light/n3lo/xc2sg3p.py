import numba as nb
import numpy as np

from .common import d9, d81


@nb.njit("f8(f8,f8[:])", cache=True)
def c2s3a(y, args):
    nf = args[0]
    flps = args[1]
    y1 = 1.0 - y
    dl = np.log(y)
    dl1 = np.log(1.0 - y)
    c2s31 = (
        (
            856.0 * d81 * dl1**4
            - 6032.0 * d81 * dl1**3
            + 130.57 * dl1**2
            - 542.0 * dl1
            + 8501.0
            - 4714.0 * y
            + 61.50 * y**2
        )
        * y1
        + dl * dl1 * (8831.0 * dl + 4162.0 * y1)
        - 15.44 * y * dl**5
        + 3333.0 * y * dl**2
        + 1615.0 * dl
        + 1208.0 * dl**2
        - 333.73 * dl**3
        + 4244.0 * d81 * dl**4
        - 40.0 * d9 * dl**5
        - 2731.82 * y1 / y
        - 414.262 * dl / y
    )
    c2s32 = (
        (
            -64.0 * d81 * dl1**3
            + 208.0 * d81 * dl1**2
            + 23.09 * dl1
            - 220.27
            + 59.80 * y
            - 177.6 * y**2
        )
        * y1
        + -dl * dl1 * (160.3 * dl + 135.4 * y1)
        - 24.14 * y * dl**3
        - 215.4 * y * dl**2
        - 209.8 * dl
        - 90.38 * dl**2
        - 3568.0 / 243.0 * dl**3
        - 184.0 * d81 * dl**4
        + 40.2426 * y1 / y
    )
    c2s3F = (
        (126.42 - 50.29 * y - 50.15 * y**2) * y1
        - 26.717
        - 320.0 * d81 * dl**2 * (dl + 5.0)
        + 59.59 * dl
        - y * dl**2 * (101.8 + 34.79 * dl + 3.070 * dl**2)
        - 9.075 * y * y1 * dl1
    ) * y
    res = nf * (c2s31 + flps * c2s3F + nf * c2s32)
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2s3c(y, args):
    nf = args[0]
    flps = args[1]
    res = -flps * nf * 11.8880
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2g3a(y, args):
    nf = args[0]
    flg = args[1]
    yi = 1.0 / y
    dl = np.log(y)
    dl1 = np.log(1.0 - y)
    c2g31 = (
        966.0 * d81 * dl1**5
        - 935.5 * d9 * dl1**4
        + 89.31 * dl1**3
        + 979.2 * dl1**2
        - 2405.0 * dl1
        + 1372.0 * (1.0 - y) * dl1**4
        - 15729.0
        - 310510.0 * y
        + 331570.0 * y**2
        - 244150.0 * y * dl**2
        - 253.3 * y * dl**5
        + dl * dl1 * (138230.0 - 237010.0 * dl)
        - 11860.0 * dl
        - 700.8 * dl**2
        - 1440.0 * dl**3
        + 2480.5 * d81 * dl**4
        - 134.0 * d9 * dl**5
        - 6362.54 * yi
        - 932.089 * dl * yi
    )
    c2g32 = (
        131.0 * d81 * dl1**4
        - 14.72 * dl1**3
        + 3.607 * dl1**2
        - 226.1 * dl1
        + 4.762
        - 190.0 * y
        - 818.4 * y**2
        - 4019.0 * y * dl**2
        - dl * dl1 * (791.5 + 4646 * dl)
        + 739.0 * dl
        + 418.0 * dl**2
        + 104.3 * dl**3
        + 809.0 * d81 * dl**4
        + 12.0 * d9 * dl**5
        + 84.423 * yi
    )
    c2g3F = (
        3.211 * dl1**2
        + 19.04 * y * dl1
        + 0.623 * (1.0 - y) * dl1**3
        - 64.47 * y
        + 121.6 * y**2
        - 45.82 * y**3
        - y * dl * dl1 * (31.68 + 37.24 * dl)
        - y * dl * (82.40 + 16.08 * dl)
        + y * dl**3 * (520.0 * d81 + 11.27 * y)
        + 60.0 * d81 * y * dl**4
    )
    res = nf * (c2g31 + nf * (c2g32 + flg * c2g3F))
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def c2g3c(y, args):
    nf = args[0]
    res = 0.625 * nf
    return res
