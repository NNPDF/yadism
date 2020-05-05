# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""

import abc


class StructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(
        self,
        name,
        ESF,
        M2hq=None,
        M2target=None,
        *,
        interpolator,
        constants,
        threshold,
        alpha_s,
        pto,
        xiR,
        xiF
    ):
        self.name = name
        self._M2hq = M2hq
        self._M2target = M2target
        self._interpolator = interpolator
        self._constants = constants
        self._threshold = threshold
        self._alpha_s = alpha_s
        self._pto = pto
        self._xiR = xiR
        self._xiF = xiF
        self._ESF = ESF
        self.__ESFs = []
        self.__ESFcache = {}

    def load(self, kinematic_configs):
        """
        .. todo::
            docs
        """
        self.__ESFs = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self.__ESFs.append(self._ESF(self, kinematics))

    def get_output(self):
        """
        .. todo::
            docs
        """
        output = []
        for esf in self.__ESFs:
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


class F2_charm(StructureFunction):
    def __init__(self, **kwargs):
        super(F2_charm, self).__init__("F2charm", ESF_F2charm, **kwargs)


class F2_bottom(StructureFunction):
    def __init__(self, **kwargs):
        super(F2_bottom, self).__init__("F2bottom", ESF_F2bottom, **kwargs)


class F2_top(StructureFunction):
    def __init__(self, **kwargs):
        super(F2_top, self).__init__("F2top", ESF_F2top, **kwargs)


class FL_charm(StructureFunction):
    def __init__(self, **kwargs):
        super(FL_charm, self).__init__("FLcharm", ESF_FLcharm, **kwargs)


class FL_bottom(StructureFunction):
    def __init__(self, **kwargs):
        super(FL_bottom, self).__init__("FLbottom", ESF_FLbottom, **kwargs)


class FL_top(StructureFunction):
    def __init__(self, **kwargs):
        super(FL_top, self).__init__("FLtop", ESF_FLtop, **kwargs)
