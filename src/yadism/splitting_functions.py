# -*- coding: utf-8 -*-
"""
Provides the Altarelli-Parisi splitting functions.

The splitting functions are defined by :eqref:`4.90`, :cite:`pink-book` and
they are organized by the outgoing and incoming particle.

Furthermore they are organized according to their
:mod:`distribution structure <yadism.esf.distribution_vec>`.

The reference for LO splitting functions is :cite:`pink-book`.

"""

import numpy as np

from eko import constants


def pqq_reg(z):
    """
    Regular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

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


def pqq_local(x):
    r"""
    Local part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

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


def pqq_sing(z):
    """
    Singular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

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


def pqg(z):
    """
    (Regular) :math:`P_{qg}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            the quark-gluon splitting function :math:`P_{qg}(z)`

    """
    return 2.0 * constants.TR * (z ** 2 + (1.0 - z) ** 2)
