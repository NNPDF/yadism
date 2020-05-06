# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""

from .structure_functions import ESFmap


class StructureFunction:
    """
        __init__.

        Parameters
        ----------
        name :
            name
        eko_components :
            eko_components
        theory_stuffs :
            theory_stuffs

        .. todo::
            docs
    """

    def __init__(self, name, runner=None, *, eko_components, theory_stuffs):
        # internal managers
        # self.name = name
        self._ESF = ESFmap[name]
        self.__runner = runner
        self.__ESFs = []
        self.__ESFcache = {}
        # external managers
        self._interpolator = eko_components["interpolator"]
        self._constants = eko_components["constants"]
        self._threshold = eko_components["threshold"]
        self._alpha_s = eko_components["alpha_s"]
        # parameters
        self._pto = theory_stuffs["pto"]
        self._xiR = theory_stuffs["xiR"]
        self._xiF = theory_stuffs["xiF"]
        self._M2hq = theory_stuffs["M2hq"]
        self._M2target = theory_stuffs["M2target"]

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
