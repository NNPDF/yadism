# -*- coding: utf-8 -*-
"""
Defines the :py:class:`StructureFunction` class.

.. todo::
    refer to the sf-esf overview
"""

from .structure_functions import ESFmap
from .structure_functions.tmc import ESFTMCmap


class StructureFunction:
    """
        Represents an abstract structure function.

        This class acts as an intermediate handler between the :py:class:`Runner`
        exposed to the outside and the :py:class:`EvaluatedStructureFunction`
        which compute the actual observable.

        The actual child class is determined by either `ESFmap` or, if TMC is
        active, by `ESFTMCmap`.

        Parameters
        ----------
            name : str
                common name, e.g. F2light, F2charm, FLbottom
            eko_components : dict
                managers dictionary that holds all created managers (which wrap
                some more complicated structure)
            theory_params : dict
                theory dictionary containing all needed parameters
    """

    def __init__(self, name, runner=None, *, eko_components, theory_params):
        # internal managers
        self.name = name
        self.__ESF = ESFmap[name] if theory_params["TMC"] == 0 else ESFTMCmap[name[:2]]
        self.__runner = runner
        self.__ESFs = []
        self.__ESFcache = {}
        # TODO wrap managers and parameters as single attributes
        # external managers
        self.interpolator = eko_components["interpolator"]
        self.constants = eko_components["constants"]
        self.threshold = eko_components["threshold"]
        self.strong_coupling = eko_components["alpha_s"]
        self.coupling_constants = eko_components["coupling_constants"]
        # parameters
        self.pto = theory_params["pto"]
        self.xiR = theory_params["xiR"]
        self.xiF = theory_params["xiF"]
        self.M2hq = theory_params["M2hq"]
        self.TMC = theory_params["TMC"]
        self.M2target = theory_params["M2target"]

    def load(self, kinematic_configs):
        """
            Loads all kinematic configurations from the run card.

            Parameters
            ----------
                kinematic_configs : list(dict)
                    run card input
        """
        self.__ESFs = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self.__ESFs.append(self.__ESF(self, kinematics)) # TODO delegate this to get_esf?

    def get_esf(self, name, kinematics, *args):
        """
            Returns a *raw* :py:class:`EvaluatedStructureFunction` instance.

            This wrappers allows

            - TMC to to access raw computations
            - heavy quark matching schemes to access their light counter parts

            It also implements an internal caching system, to speed up the integrals
            in TMC.

            Parameters
            ----------
                name : string
                    structure function name
                kinematics : dict
                    kinematic configuration
                args : any
                    further arguments passed down to the instance

            Returns
            -------
                obj : EvaluatedStructureFunction
                    created object
        """
        # is it us or do we need to delegate?
        if name == self.name:
            # convert to tuple
            key = tuple(kinematics.values()) # TODO how to incorporate args?
            # search
            try:
                return self.__ESFcache[key]
            except KeyError:
                obj = ESFmap[name](self, kinematics, *args)
                self.__ESFcache[key] = obj
                return obj
        else:
            # ask our parent (as always)
            return self.__runner.observable_instances[name].get_esf(
                name, kinematics, *args
            )

    def get_output(self):
        """
            Collects the output from all childrens.

            Returns
            -------
                output : list(dict)
                    all children outputs
        """
        output = []
        for esf in self.__ESFs:
            output.append(esf.get_output())

        return output