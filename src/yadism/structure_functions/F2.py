# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.
"""

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF


class ESF_F2(ESF):
    def __init__(self, interpolator, kinematics):
        super(ESF_F2, self).__init__(interpolator=interpolator, kinematics=kinematics)

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

        """

        # leading order is just a delta function
        return polynomial_f(self._x)
