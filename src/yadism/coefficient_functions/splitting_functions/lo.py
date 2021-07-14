# -*- coding: utf-8 -*-
"""
Provides the Altarelli-Parisi splitting functions.

The splitting functions are defined by :cite:`split-ns,split-singlet` and
they are organized by the outgoing and incoming particle.
Furthermore they are organized according to their RSL structure.

"""

import numba as nb
import numpy as np
from eko import constants

from ..partonic_channel import RSL


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq_reg(z, _args):
    """
    Regular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.5`, :cite:`split-ns`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            the regular bit of quark-quark splitting function :math:`P_{qq}^R(z)`

    """
    return -2.0 * constants.CF * (1.0 + z)


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq_sing(z, _args):
    """
    Singular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.5`, :cite:`split-ns`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            the singular bit the quark-quark splitting function :math:`P_{qq}^S(z)`
    """
    return 4.0 * constants.CF / (1.0 - z)


@nb.njit("f8(f8,f8[:])", cache=True)
def pqq_local(x, _args):
    r"""
    Local part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.5`, :cite:`split-ns`.

    Parameters
    ----------
        x : float
            hadronic momentum fraction

    Returns
    -------
        float
            the local bit of quark-quark splitting function :math:`P_{qq}^L(x)`

    """
    return constants.CF * (3.0 + 4.0 * np.log(1.0 - x))


def pqq(_nf):
    """
    :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.5`, :cite:`split-ns`.

    Parameters
    ----------
        nf : int
            number of active flavors

    Returns
    -------
        RSL
            the quark-quark splitting function :math:`P_{qq}(z)`
    """
    return RSL(pqq_reg, pqq_sing, pqq_local)


@nb.njit("f8(f8,f8[:])", cache=True)
def pqg_single(z, _args):
    """
    :math:`P_{q_ig}` splitting function (i.e.: :math:`P_{qg}` for a single
    flavor).

    |ref| implements :eqref:`4.6` and :eqref:`2.5`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            the quark-gluon splitting function :math:`P_{q_ig}(z)`

    """
    return 2.0 * constants.TR * (z ** 2 + (1.0 - z) ** 2)


@nb.njit("f8(f8,f8[:])", cache=True)
def pqg_reg(z, args):
    """
    (Regular) :math:`P_{qg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            the quark-gluon splitting function :math:`P_{qg}(z)`

    """
    return 2 * args[0] * pqg_single(z, args)


def pqg(nf):
    """
    :math:`P_{qg}` splitting function.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        nf : int
            number of active flavors

    Returns
    -------
        RSL
            the quark-gluon splitting function :math:`P_{qg}(z)`

    """
    return RSL(pqg_reg, args=[nf])


raw_labels = {"P_qq_0": pqq, "P_qg_0": pqg}
