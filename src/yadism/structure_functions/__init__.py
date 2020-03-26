# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.
"""

from . import EvaluatedStructureFunction
from .F2 import ESF_F2
from .FL import ESF_FL

import abc


class StructureFunction(abc.ABC):
    def __init__(self, name, ESF, interpolator):
        self._name = name
        self._interpolator = interpolator
        self._ESF = ESF
        self._ESFS = []

    def load(self, kinematic_configs):
        self._ESFS = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self._ESFS.append(self._ESF(self._interpolator, kinematics))

    def get_output(self):
        output = []
        for esf in self._ESFS:
            output.append(esf.get_output())

        return output


class F2(StructureFunction):
    def __init__(self, interpolator):
        super(F2, self).__init__("F2", ESF_F2, interpolator)


class FL(StructureFunction):
    def __init__(self, interpolator):
        super(FL, self).__init__("FL", ESF_FL, interpolator)
