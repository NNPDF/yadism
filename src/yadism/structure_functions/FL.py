# -*- coding: utf-8 -*-
"""
"""

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF


class ESF_FL(ESF):
    def __init__(self, interpolator, kinematics):
        super(ESF_FL, self).__init__(interpolator=interpolator, kinematics=kinematics)

    def light_LO_quark(self, polynomial_f) -> float:
        return 0
