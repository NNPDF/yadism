# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""

from .structure_functions import ESFmap
from .structure_functions.tmc import ESFTMCmap


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
        self._name = name
        self.__ESF = ESFmap[name] if theory_stuffs["TMC"] == 0 else ESFTMCmap[name[:2]]
        self.__runner = runner
        self.__ESFs = []
        self.__ESFcache = {}
        # external managers
        self.interpolator = eko_components["interpolator"]
        self.constants = eko_components["constants"]
        self.threshold = eko_components["threshold"]
        self.strong_coupling = eko_components["alpha_s"]
        self.coupling_constants = eko_components["coupling_constants"]
        # parameters
        self.pto = theory_stuffs["pto"]
        self.xiR = theory_stuffs["xiR"]
        self.xiF = theory_stuffs["xiF"]
        self.M2hq = theory_stuffs["M2hq"]
        self.TMC = theory_stuffs["TMC"]
        self.M2target = theory_stuffs["M2target"]

    def load(self, kinematic_configs):
        """
        .. todo::
            docs
        """
        self.__ESFs = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self.__ESFs.append(self.__ESF(self, kinematics))

    def get_ESF(self, name, kinematics):
        """
            get_ESF.

            Parameters
            ----------
            name :
                name
            kinematics :
                kinematics

            .. todo::
                docs
        """
        # is it us or do we need to delegate?
        if name == self._name:
            # convert to tuple
            key = tuple(kinematics.values())
            # search
            try:
                return self.__ESFcache[key]
            except KeyError:
                obj = ESFmap[name](self, kinematics)
                self.__ESFcache[key] = obj
                return obj
        else:
            # ask our parent (as always)
            return self.__runner.observable_instances[name].get_ESF(name, kinematics)

    def get_output(self):
        """
        .. todo::
            docs
        """
        output = []
        for esf in self.__ESFs:
            output.append(esf.get_output())

        return output
