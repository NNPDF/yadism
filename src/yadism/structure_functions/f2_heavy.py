# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .esf import EvaluatedStructureFunctionHeavy as ESFH


class EvaluatedStructureFunctionF2heavy(ESFH):
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


class EvaluatedStructureFunctionF2charm(EvaluatedStructureFunctionF2heavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2charm, self).__init__(SF, kinematics, charge_em=2 / 3)


class EvaluatedStructureFunctionF2bottom(EvaluatedStructureFunctionF2heavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2bottom, self).__init__(SF, kinematics, charge_em=1 / 3)


class EvaluatedStructureFunctionF2top(EvaluatedStructureFunctionF2heavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2top, self).__init__(SF, kinematics, charge_em=2 / 3)
