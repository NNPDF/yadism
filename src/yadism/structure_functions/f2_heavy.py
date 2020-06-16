# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quark flavours.

Differently from the :py:mod:`F2heavy` here more classes are provided, since
its flavour can be individually selected. Nevertheless a common class is also
defined, :py:class:`ESF_F2heavy`, to factorize all the common structure related
to heavy flavours; the common class is a further intermediate node in the
hierarchy, since it is a direct child of :py:class:`ESFH` (it is actually the
F2 flavoured version of :py:class:`ESFH`) at it is the direct ancestor for the
individual flavour ones.

Actually the coefficient functions formulas are encoded already at the level of
:py:class:`ESF_F2heavy`, while the explicit leaf classes are used to handle the
differences between flavours (e.g. electric charge).

The main reference used is: :cite:`felix-thesis`.

"""

import numpy as np

from .esf import EvaluatedStructureFunctionHeavy as ESFH


class EvaluatedStructureFunctionF2heavy(ESFH):
    """
        Compute F2 structure functions for heavy quark flavours.

        This class inherits from :py:class:`EvaluatedStructureFunctionHeavy`,
        providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent (and, mainly, in its own parent).

        Even if this is still an intermediate class it has already enough
        information to be able to express coefficient functions, while children
        are used just ot handle differences among flavours (e.g. electric
        charge).

    """

    def _gluon_1(self):
        """
            Computes the gluon part of the next to leading order F2 structure
            function.

            |ref| implements :eqref:`D.1`, :cite:`felix-thesis`.

            Returns
            -------
                sequence of callables
                    coefficient functions, as two arguments functions: :py:`(x, Q2)`

            Note
            ----
                Immediately check if the available energy is below threshold for
                flavour production (no other calculation is needed nor performed in
                this case).

        """

        def cg(z):
            if self.is_below_threshold(z):
                return 0
            # fmt: off
            return self._FHprefactor * (
                (-np.pi * self._rho_p(z) ** 3)
                / (4 * self._rho(z) ** 2 * self._rho_q ** 2)
                * (
                    2 * self._beta(z) * (
                        self._rho(z) ** 2
                        + self._rho_q ** 2
                        + self._rho(z) * self._rho_q * (6 + self._rho_q)
                    )
                    +
                    np.log(self._chi(z)) * (
                        2 * self._rho_q ** 2 * (1 + self._rho(z))
                        + self._rho(z) ** 2 * (2 - (self._rho_q - 4) * self._rho_q)
                    )
                )) / z
            # fmt: on

        return cg


class EvaluatedStructureFunctionF2charm(EvaluatedStructureFunctionF2heavy):
    """
        Compute F2 structure functions for *charm* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2heavy`.
        Currently this class sets only:

        - nhq = 4

    """

    def __init__(self, SF, kinematics, force_local):
        super(EvaluatedStructureFunctionF2charm, self).__init__(
            SF, kinematics, 4, force_local
        )


class EvaluatedStructureFunctionF2bottom(EvaluatedStructureFunctionF2heavy):
    """
        Compute F2 structure functions for *bottom* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2heavy`.
        Currently this class sets only:

        - nhq = 5

    """

    def __init__(self, SF, kinematics, force_local):
        super(EvaluatedStructureFunctionF2bottom, self).__init__(
            SF, kinematics, 5, force_local
        )


class EvaluatedStructureFunctionF2top(EvaluatedStructureFunctionF2heavy):
    """
        Compute F2 structure functions for *top* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2heavy`.
        Currently this class sets only:

        - nhq = 6

    """

    def __init__(self, SF, kinematics, force_local):
        super(EvaluatedStructureFunctionF2top, self).__init__(
            SF, kinematics, 6, force_local
        )
