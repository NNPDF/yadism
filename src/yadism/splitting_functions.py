# -*- coding: utf-8 -*-
"""
Provides splitting functions definition for coefficient functions calculation.

The coefficient functions are defined in :eqref:`4.87`, :cite:`pink-book`, and
they are organized in:

- qq
- qg
- gq
- gg

according to the partons (entering the hard process - coming from the proton).

Furthermore they are organized according to their distribution structure, for
which see :py:mod:`convolution`.

The reference for LO splitting functions is :cite:`pink-book`.

.. todo:: rewrite pqq in RSL fashion

"""

import numpy as np

from eko import constants


def pqq_reg(z):
    """
    The expression of the regular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

    Parameters
    ----------
        z : float
            momentum fraction

    Returns
    -------
        float
            the regular bit of pqq splitting function @ :py:`z`

    """
    return -2.0 * constants.CF * (1.0 + z)


def pqq_local(x):
    r"""
    The expression of the local part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

    Parameters
    ----------
        x : float
            momentum fraction

    Returns
    -------
        float
            the locacl bit of pqq splitting function @ :py:`x`

    """
    return constants.CF * (3.0 + 4.0 * np.log(1.0 - x))


def pqq_sing(z):
    """
    The expression of the singular part of :math:`P_{qq}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pink-book`.

    Parameters
    ----------
        z : float
            momentum fraction

    Returns
    -------
        float
            the singular bit of pqq splitting function @ :py:`z`

    """
    return 4.0 * constants.CF / (1.0 - z)


def pqg(z):
    """
    The expression of :math:`P_{qg}` splitting function.

    |ref| implements :eqref:`4.94`, :cite:`pegasus`.

    Parameters
    ----------
        z : float
            momentum fraction

    Returns
    -------
        float
            the pqg splitting function @ :py:`z`

    """
    return 2.0 * constants.TR * (z ** 2 + (1.0 - z) ** 2)
