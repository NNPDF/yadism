# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
light quark flavours (namely *up*, *bottom*, *strange*).

The only element present is the :py:class:`ESF_F2light`, that inherits the
:py:class:`EvaluatedStructureFunction` machinery, but it is used just to store
the definitions of the related coefficient functions formula.

The main reference used is: :cite:`felix-thesis`.

.. todo:
    - light -> heavy
    - reference is thesis, not vogt

"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunctionHeavy as ESFH


class ESF_F2heavy(ESFH):
    """
    .. todo::
        docs
    """

    def _gluon_1(self):
        """

        .. todo::
            docs
        """
        CF = self._SF.constants.CF

        def cg(z):
            if self.is_below_threshold(z):
                return 0
            # fmt: off
            return self._FHprefactor * self._charge_em ** 2 * (
                3 * CF / 4
                * (-np.pi * self._rho_p(z) ** 3)
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


class ESF_F2charm(ESF_F2heavy):
    def __init__(self, SF, kinematics):
        super(ESF_F2charm, self).__init__(SF, kinematics, charge_em=2 / 3)


class ESF_F2bottom(ESF_F2heavy):
    def __init__(self, SF, kinematics):
        super(ESF_F2bottom, self).__init__(SF, kinematics, charge_em=1 / 3)


class ESF_F2top(ESF_F2heavy):
    def __init__(self, SF, kinematics):
        super(ESF_F2top, self).__init__(SF, kinematics, charge_em=2 / 3)
