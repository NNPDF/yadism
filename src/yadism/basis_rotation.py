# -*- coding: utf-8 -*-
"""
This module contains the definitions of the different basis used, i.e.:

- Physical basis::

    -7  -6  -5  -4  -3  -2  -1   0   1   2   3   4   5   6
    gm  tb  bb  cb  sb  ub  db   g   d   u   s   c   b   t

- QCD Evolution basis::

    0   1   2   3   4   5   6   7   8   9  10  11  12  13
    gm  Sg   g   V  V3  V8 V15 V24 V35  T3  T8 T15 T24 T35


Notes
-----
The name of the matrices are taken from those originally used in APFEL
replacing the format::

    ${basis1}2${basis2}  --> ${basis2}4${basis1}

because in this way the matrix algebra is more clear.
"""

import numpy as np


# Tranformation from physical basis to QCD evolution basis
TevQCD4ph = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, -0, -1, 1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, 0, 2, -1, -1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, 3, -1, -1, -1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, 4, -1, -1, -1, -1, 0, 1, 1, 1, 1, -4, 0],
        [0, 5, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, -5],
        [0, 0, 0, -0, 0, 1, -1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, -0, -2, 1, 1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, -3, 1, 1, 1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, -4, 1, 1, 1, 1, 0, 1, 1, 1, 1, -4, 0],
        [0, -5, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, -5],
    ]
)

# Tranformation from QCD evolution basis to physical basis
Tph4evQCD = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, -0, -1, 1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, 0, 2, -1, -1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, 3, -1, -1, -1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, 4, -1, -1, -1, -1, 0, 1, 1, 1, 1, -4, 0],
        [0, 5, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, -5],
        [0, 0, 0, -0, 0, 1, -1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, -0, -2, 1, 1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, -3, 1, 1, 1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, -4, 1, 1, 1, 1, 0, 1, 1, 1, 1, -4, 0],
        [0, -5, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, -5],
    ]
)

# Evolution basis


def QCDsinglet(ph):
    """Project the physical basis on the singlet.

    Parameters
    ----------
    ph : sequence (length 14)
        Description of parameter `ph`.

    Returns
    -------
    type
        Description of returned object.

    """

    return TevQCD4ph[1] @ np.array(ph)


def QCDT3(ph):
    """Short summary.

    Parameters
    ----------
    ph : sequence (length 14)
        Description of parameter `ph`.

    Returns
    -------
    type
        Description of returned object.

    """

    return TevQCD4ph[9] @ np.array(ph)


def QCDT8(ph):
    """Short summary.

    Parameters
    ----------
    ph : sequence (length 14)
        Description of parameter `ph`.

    Returns
    -------
    type
        Description of returned object.

    """

    return TevQCD4ph[10] @ np.array(ph)


def QCDV3(ph):
    """Short summary.

    Parameters
    ----------
    ph : sequence (length 14)
        Description of parameter `ph`.

    Returns
    -------
    type
        Description of returned object.

    """

    return TevQCD4ph[4] @ np.array(ph)
