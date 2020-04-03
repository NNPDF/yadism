# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split


class ESF_FLlight(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        super(ESF_FLlight, self).__init__(SF, kinematics)

    def quark_0(self) -> float:
        """
        .. todo::
            docs
        """

        return 0

    def gluon_0(self) -> float:
        """
        .. todo::
            docs
        """
        return 0

    def quark_1(self):
        """
        regular
        delta
        1/(1-x)_+
        log(x)/(1-x)_+

        .. todo::
            docs
        """
        CF = self._SF._constants.CF
        zeta_2 = np.pi ** 2 / 6

        def cq_reg(z):
            return CF * 4 * z

        return cq_reg

    def gluon_1(self):
        """
        vogt page 117

        .. todo::
            docs
        """

        def cg(z):
            return self._n_f * (8 * z * (1 - z))

        return cg
