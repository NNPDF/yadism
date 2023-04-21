import numba as nb
import numpy as np

from .common import d27, d81


@nb.njit("f8(f8,f8[:])", cache=True)
def cls3a(y, args):
    nf = args[0]
    flps = args[1]
    dl = np.log(y)
    y1 = 1.0 - y
    dl1 = np.log(1.0 - y)

    cls31 = (
        (1568.0 * d27 * dl1**3 - 11904.0 * d27 * dl1**2 + 5124.0 * dl1) * y1**2
        + dl * dl1 * (2184.0 * dl + 6059.0 * y1)
        - (795.6 + 1036.0 * y) * y1**2
        - 143.6 * dl * y1
        + 8544.0 * d27 * dl**2
        - 1600.0 * d27 * dl**3
        - 885.53 / y * y1**2
        - 182.00 * dl / y * y1
    )
    cls32 = (
        (-96.0 * d27 * dl1**2 + 29.52 * dl1) * y1**2
        + +dl * dl1 * (35.18 * dl + 73.06 * y1)
        - (14.16 - 69.84 * y) * y1**2
        - 35.24 * y * dl**2
        - 69.41 * dl * y1
        - 384.0 * d27 * dl**2
        + 40.239 / y * y1**2
    )
    cls3F = (
        (107.0 + 321.05 * y - 54.62 * y**2) * (1.0 - y)
        - 26.717
        - 320.0 * d81 * dl**3
        - 640.0 * d81 * dl**2
        + 9.773 * dl
        + y * dl * (363.8 + 68.32 * dl)
    ) * y
    # Note here the source file cointain a typo and the
    # proper color factor is flps = fls - fl, not just fls.
    # see https://arxiv.org/pdf/hep-ph/0411112.pdf eq 9.
    res = nf * (cls31 + (flps) * cls3F + nf * cls32)
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def clg3a(y, args):
    nf = args[0]
    flg = args[1]
    dl = np.log(y)
    y1 = 1.0 - y
    dl1 = np.log(1.0 - y)

    clg31 = (
        (
            144.0 * dl1**4
            - 47024.0 * d27 * dl1**3
            + 6319.0 * dl1**2
            + 53160.0 * dl1
        )
        * y1
        + dl * dl1 * (72549.0 + 88238.0 * dl)
        + (3709.0 - 33514.0 * y - 9533.0 * y**2) * y1
        + 66773.0 * y * dl**2
        - 1117.0 * dl
        + 45.37 * dl**2
        - 5360.0 * d27 * dl**3
        - 2044.70 / y * y1
        - 409.506 * dl / y
    )
    clg32 = (
        (
            288.0 * d27 * dl1**3
            - 3648.0 * d27 * dl1**2
            - 592.3 * dl1
            + 1511.0 * y * dl1
        )
        * y1
        + dl * dl1 * (311.3 + 14.24 * dl)
        + (577.3 - 729.0 * y) * y1
        + 30.78 * y * dl**3
        + 366.0 * dl
        + 3000.0 * d27 * dl**2
        + 480.0 * d27 * dl**3
        + 88.5037 / y * y1
    )
    clg3F = (
        (
            -0.0105 * dl1**3
            + 1.550 * dl1**2
            + 19.72 * y * dl1
            - 66.745 * y
            + 0.615 * y**2
        )
        * y1
        + 20.0 * d27 * y * dl**4
        + (280.0 / 81.0 + 2.260 * y) * y * dl**3
        - (15.40 - 2.201 * y) * y * dl**2
        - (71.66 - 0.121 * y) * y * dl
    )
    res = nf * (clg31 + nf * (clg32 + flg * clg3F))
    return res
