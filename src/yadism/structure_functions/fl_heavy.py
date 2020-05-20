# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .esf import EvaluatedStructureFunctionHeavy as ESFH


class EvaluatedStructureFunctionFLheavy(ESFH):
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
            return  self._FHprefactor * self._charge_em ** 2 * (
                3 * CF / 4
                * (-np.pi * self._rho_p(z) ** 3) / (self._rho(z) * self._rho_q)
                * (2 * self._beta(z) + self._rho(z) * np.log(self._chi(z)))
            ) / z
            # fmt: on

        return cg


class EvaluatedStructureFunctionFLcharm(EvaluatedStructureFunctionFLheavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLcharm, self).__init__(SF, kinematics, charge_em=2 / 3)


class EvaluatedStructureFunctionFLbottom(EvaluatedStructureFunctionFLheavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLbottom, self).__init__(SF, kinematics, charge_em=1 / 3)


class EvaluatedStructureFunctionFLtop(EvaluatedStructureFunctionFLheavy):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLtop, self).__init__(SF, kinematics, charge_em=2 / 3)
