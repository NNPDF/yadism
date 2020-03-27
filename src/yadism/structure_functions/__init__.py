# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.

.. todo::
    docs
"""

from . import EvaluatedStructureFunction
from .F2 import ESF_F2
from .FL import ESF_FL

import abc


class StructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(self, name, ESF, *, interpolator, constants, threshold, alpha_s, pto):
        self._name = name
        self._interpolator = interpolator
        self._constants = constants
        self._threshold = threshold
        self._alpha_s = alpha_s
        self._pto = pto
        self._ESF = ESF
        self.__ESFS = []

    def load(self, kinematic_configs):
        """
        .. todo::
            docs
        """
        self.__ESFS = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self.__ESFS.append(self._ESF(self, kinematics))

    def get_output(self):
        """
        .. todo::
            docs
        """
        output = []
        for esf in self.__ESFS:
            output.append(esf.get_output())

        return output


class F2(StructureFunction):
    """
    .. todo::
        docs
    """

    def __init__(self, **kwargs):
        super(F2, self).__init__("F2", ESF_F2, **kwargs)


class FL(StructureFunction):
    """
    .. todo::
        docs
    """

    def __init__(self, **kwargs):
        super(FL, self).__init__("FL", ESF_FL, **kwargs)
