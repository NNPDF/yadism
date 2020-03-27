# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
import abc

import numpy as np


class EvaluatedStructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(self, interpolator, kinematics):
        if 1 < kinematics["x"] < 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1)")
        if kinematics["Q2"] < 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")

        self._interpolator = interpolator
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        self._cqv = []
        self._cgv = []

    def _compute(self):
        """
        .. todo::
            docs
        """
        # something to do?
        if self._cqv:
            # nothing to do
            return

        # iterate all polynomials
        for polynomial_f in self._interpolator:
            self._cqv.append(self.light_LO_quark(polynomial_f))

    def get_output(self):
        """
        .. todo::
            docs
        """
        self._compute()

        output = {}
        output["x"] = self._x
        output["Q2"] = self._Q2
        output["q"] = self._cqv
        output["g"] = self._cgv
        return output

    @abc.abstractclassmethod
    def light_LO_quark(self, polynomial_f):
        """
        .. todo::
            docs
        """
        pass
