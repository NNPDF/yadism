# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split, convolution as conv


class ESF_FL(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        super(ESF_FL, self).__init__(SF, kinematics)

    def light_LO_quark(self, polynomial_f) -> float:
        """
        .. todo::
            docs
        """

        # leading order is just a delta function
        return 0

    def light_LO_gluon(self, polynomial_f) -> float:
        """
        .. todo::
            docs
        """
        return 0

    def light_NLO_quark(self, polynomial_f):
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

        cq_dvec = conv.DistributionVec(cq_reg)
        return conv.convnd(self._x, cq_dvec, polynomial_f)[0]

    def light_NLO_gluon(self, polynomial_f):
        """
        vogt page 117

        .. todo::
            docs
        """

        def cg(z):
            return self._n_f * (8 * z * (1 - z))

        cg_dvec = conv.DistributionVec(cg)
        return conv.convnd(self._x, cg_dvec, polynomial_f)[0]
