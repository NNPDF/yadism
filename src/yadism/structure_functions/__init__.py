# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.

.. todo::
    docs
"""

from . import EvaluatedStructureFunction
from .F2light import ESF_F2light
from .FLlight import ESF_FLlight
from .FLheavy import ESF_FLcharm, ESF_FLbottom

import abc


class StructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(
        self, name, ESF, M2=None, *, interpolator, constants, threshold, alpha_s, pto
    ):
        self.name = name
        self._M2 = M2
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


class F2_light(StructureFunction):
    """
    .. todo::
        docs
    """

    def __init__(self, **kwargs):
        super(F2_light, self).__init__("F2light", ESF_F2light, **kwargs)


class FL_light(StructureFunction):
    """
    .. todo::
        docs
    """

    def __init__(self, **kwargs):
        super(FL_light, self).__init__("FLlight", ESF_FLlight, **kwargs)


# class F2_charm(StructureFunction):
# def __init__(self, **kwargs):
# super(F2_charm, self).__init__("F2charm", ESF_F2charm, **kwargs)


class FL_charm(StructureFunction):
    def __init__(self, **kwargs):
        super(FL_charm, self).__init__("FLcharm", ESF_FLcharm, **kwargs)


class FL_bottom(StructureFunction):
    def __init__(self, **kwargs):
        super(FL_bottom, self).__init__("FLbottom", ESF_FLbottom, **kwargs)
