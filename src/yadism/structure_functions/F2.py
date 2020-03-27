# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split, convolution as conv


class ESF_F2(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        super(ESF_F2, self).__init__(SF, kinematics)

    def light_LO_quark(self, polynomial_f) -> float:
        """Computes the singlet part of the leading order F2 structure function.

        Implements equation 4.2 of :cite:`Vermaseren:2005qc`.

        Parameters
        ----------
        x : float
            Bjorken x
        Q2 : float
            squared(!) momentum transfer
        polynom_f : func
            interpolation polynomial

        Returns
        -------
        float
            F2(x,Q^2)

        .. todo::
            docs
        """

        # leading order is just a delta function
        return polynomial_f(self._x)

    def light_LO_gluon(self, polynomial_f) -> float:
        """
        .. todo::
            docs
        """
        return 0

    def light_NLO_quark(self, polynomial_f):
        """
        .. todo::
            docs
        """
        return 0
        # Missing convolution

        # regular
        # delta
        # 1/(1-x)_+
        # log(x)/(1-x)_+

    def light_NLO_gluon(self, polynomial_f):
        """
        .. todo::
            docs
        """

        TR = self._SF._constants.TF

        def cg(z):
            return split.pqg(z) * (np.log((1 - z) / z) - 4) + 3 * TR

        cg_dvec = conv.DistributionVec(cg)
        return conv.convnd(self._x, cg_dvec, polynomial_f)[0]
