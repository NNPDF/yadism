import numba as nb
import numpy as np
from eko import constants

from ... import special


@nb.njit("f8(f8,f8[:])", cache=True)
def pnsm_reg(z, args):
    """
    Regular :math:`P_{ns,-}` non-singlet valence-like splitting function (common
    to minus and valence).

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the non-singlet valence-like splitting function :math:`P_{ns,-}(z)`

    """
    x = z
    NF = args[0]
    zeta2 = special.zeta2
    S2 = special.s2
    CF = constants.CF
    CA = constants.CA

    lnx = np.log(x)
    ln1mx = np.log(1 - x)
    pqq = 2 / (1 - x) - 1 - x
    pqqmx = 2 / (1 + x) - 1 + x
    S2x = S2(x)
    DM = 1 / (1 - x)

    # fmt: off
    GQQ1 = (
        2 * CF * NF * ( ( - 1.1111111111111112 - ( 2 * lnx )
        / 3 ) * pqq - ( 4 * ( 1 - x ) ) / 3 )
        + 4 * CA * CF * ( ( 3.7222222222222223 + ( 11 * lnx )
        / 6 + lnx**2 / 2 - np.pi**2 / 6 ) * pqq
        + ( 20 * ( 1 - x ) ) / 3 + lnx * ( 1 + x) )
        + 4 * CF**2 * ( ( ( - 3 * lnx ) / 2 - 2 * ln1mx
        * lnx ) * pqq - 5 * ( 1 - x ) - ( lnx**2 * ( 1
        + x ) ) / 2 - lnx * ( 1.5 + ( 7 * x ) / 2 ) )
        - 4 * CF * ( CF - CA / 2 ) * ( 2 * pqqmx * S2x
        + 4 * ( 1 - x ) + 2 * lnx * ( 1 + x ) )
    )
    # fmt: on

    #  The soft (`+'-distribution) part of the splitting function

    A2 = -40 / 9 * CF * NF + 268 / 9 * CA * CF - 8 * zeta2 * CA * CF

    GQQ1L = DM * A2

    #  The regular piece of the coefficient function

    X1NSMA = GQQ1 - GQQ1L

    return X1NSMA


@nb.njit("f8(f8,f8[:])", cache=True)
def pnsp_reg(z, args):
    """
    Regular :math:`P_{ns,+}` non-singlet singlet-like splitting function.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the non-singlet singlet-like splitting function :math:`P_{ns,+}(z)`

    """
    x = z
    NF = args[0]
    zeta2 = special.zeta2
    S2 = special.s2
    CF = constants.CF
    CA = constants.CA

    lnx = np.log(x)
    ln1mx = np.log(1 - x)
    pqq = 2 / (1 - x) - 1 - x
    pqqmx = 2 / (1 + x) - 1 + x
    S2x = S2(x)
    DM = 1 / (1 - x)

    # fmt: off
    GQQ1 = (
        2 * CF * NF * ( ( - 1.1111111111111112 - ( 2 * lnx )
        / 3 ) * pqq - ( 4 * ( 1 - x ) ) / 3 )
        + 4 * CA * CF * ( ( 3.7222222222222223 + ( 11 * lnx )
        / 6 + lnx**2 / 2 - np.pi**2 / 6 ) * pqq
        + ( 20 * ( 1 - x ) ) / 3 + lnx * ( 1 + x) )
        + 4 * CF**2 * ( ( ( - 3 * lnx ) / 2 - 2 * ln1mx
        * lnx ) * pqq - 5 * ( 1 - x ) - ( lnx**2 * ( 1
        + x ) ) / 2 - lnx * ( 1.5 + ( 7 * x ) / 2 ) )
        + 4 * CF * ( CF - CA / 2 ) * ( 2 * pqqmx * S2x
        + 4 * ( 1 - x ) + 2 * lnx * ( 1 + x ) )
    )
    # fmt: on

    #  The soft (`+'-distribution) part of the splitting function

    A2 = -40 / 9 * CF * NF + 268 / 9 * CA * CF - 8 * zeta2 * CA * CF

    GQQ1L = DM * A2

    #  The regular piece of the coefficient function

    X1NSPA = GQQ1 - GQQ1L

    return X1NSPA


@nb.njit("f8(f8,f8[:])", cache=True)
def pns_sing(z, args):
    """
    Singular :math:`P_{ns}` non-singlet splitting function (common to plus,
    minus, and valence).

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the non-singlet splitting function :math:`P_{ns}(z)`

    """
    Y = z
    NF = args[0]
    zeta2 = special.zeta2
    CF = constants.CF
    CA = constants.CA

    A2 = -40 / 9 * CF * NF + 268 / 9 * CA * CF - 8 * zeta2 * CA * CF
    X1NSB = A2 / (1 - Y)

    return X1NSB


@nb.njit("f8(f8,f8[:])", cache=True)
def pns_loc(x, args):
    """
    Local :math:`P_{ns}` non-singlet splitting function (common to plus,
    minus, and valence).

    Parameters
    ----------
        x : float
            Bjorken :math:`x`
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the non-singlet splitting function :math:`P_{ns}(z)`

    """
    Y = x
    NF = args[0]
    zeta2 = special.zeta2
    zeta3 = special.zeta3
    CF = constants.CF
    CA = constants.CA

    # fmt: off
    P1DELT =(
        - 1/3*CF*NF
        + 3/2*CF**2
        + 17/6*CA*CF
        + 24*zeta3*CF**2
        - 12*zeta3*CA*CF
        - 8/3*zeta2*CF*NF
        - 12*zeta2*CF**2
        + 44/3*zeta2*CA*CF
    )
    # fmt: on

    #  The soft (`+'-distribution) part of the splitting function

    A2 = -40 / 9 * CF * NF + 268 / 9 * CA * CF - 8 * zeta2 * CA * CF

    X1NSC = np.log(1 - Y) * A2 + P1DELT

    return X1NSC
