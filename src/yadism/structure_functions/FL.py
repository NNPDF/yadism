# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF


class ESF_FL(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, interpolator, kinematics):
        super(ESF_FL, self).__init__(interpolator=interpolator, kinematics=kinematics)

    def light_LO_quark(self, polynomial_f) -> float:
        """
        .. todo::
            docs
        """
        return 0
