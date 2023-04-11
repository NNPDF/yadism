import numba as nb
import numpy as np
from eko import constants

from ... import special
from . import non_singlet as ns


@nb.njit("f8(f8,f8[:])", cache=True)
def pgq0_reg(z, _args):
    """
    (Regular) :math:`P_{gq}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the gluon-quark splitting function :math:`P_{gq}(z)`

    """
    return 2.0 * constants.CF * (2 / z - 2 + z)


@nb.njit("f8(f8,f8[:])", cache=True)
def pgg0_reg(z, _args):
    """
    Regular :math:`P_{gg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the gluon-gluon splitting function :math:`P_{gg}(z)`

    """
    return 4 * constants.CA * (1 / z - 2 + z - z**2)


@nb.njit("f8(f8,f8[:])", cache=True)
def pgg0_sing(z, _args):
    """
    Singular :math:`P_{gg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the gluon-gluon splitting function :math:`P_{gg}(z)`

    """
    return 4 * constants.CA / (1 - z)


@nb.njit("f8(f8,f8[:])", cache=True)
def pgg0_local(x, args):
    """
    Singular :math:`P_{gg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the gluon-gluon splitting function :math:`P_{gg}(z)`

    """
    return constants.CA * (4 * np.log(1 - x) + 11 / 3) - args[0] * 2 / 3


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq1ps_reg(z, args):
    """
    Regular :math:`P_{qq}` pure singlet splitting function.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the quark-quark pure singlet splitting function :math:`P_{qq}(z)`

    """
    nf = args[0]
    x = z

    DX = 1 / x
    LNX = np.log(x)
    HR200 = LNX * LNX / 2

    #  The splitting function in terms of the harmonic polylogs
    X1PSA = (
        +nf
        * constants.CF
        * (
            -8
            + 24 * x
            - 224 / 9 * x**2
            + 80 / 9 * DX
            + 4 * LNX
            + 20 * LNX * x
            + 32 / 3 * LNX * x**2
            - 8 * HR200
            - 8 * HR200 * x
        )
    )

    return X1PSA


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq1_reg(z, args):
    """
    Regular :math:`P_{qq}` splitting function.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the quark-quark singlet splitting function :math:`P_{qq}(z)`

    """
    return pqq1ps_reg(z, args) + ns.pnsp_reg(z, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def pqg1_reg(z, args):
    """
    (Regular) :math:`P_{qg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        args : np.ndarray
            further arguments

    Returns
    -------
        float
            the quark-gluon splitting function :math:`P_{qg}(z)`

    """
    CA = constants.CA
    CF = constants.CF
    NF = args[0]
    x = z

    lnx = np.log(x)
    ln1mx = np.log(1 - x)
    pqg = x**2 + (1 - x) ** 2
    pqgmx = x**2 + (1 + x) ** 2
    S2x = special.s2(x)

    X1QGA = 2 * CF * NF * (
        4
        + 4 * ln1mx
        + (10 - 4 * (ln1mx - lnx) + 2 * (-ln1mx + lnx) ** 2 - 2 * np.pi**2 / 3) * pqg
        - lnx * (1 - 4 * x)
        - lnx**2 * (1 - 2 * x)
        - 9 * x
    ) + 2 * CA * NF * (
        20.22222222222222
        - 4 * ln1mx
        + (
            -24.22222222222222
            + 4 * ln1mx
            - 2 * ln1mx**2
            + (44 * lnx) / 3
            - lnx**2
            + np.pi**2 / 3
        )
        * pqg
        + 2 * pqgmx * S2x
        + 40 / (9 * x)
        + (14 * x) / 9
        - lnx**2 * (2 + 8 * x)
        + lnx * (-12.666666666666666 + (136 * x) / 3)
    )
    return X1QGA
