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
            obs_name : .observable_name.ObservableName
                name
            eko_components : dict
                managers dictionary that holds all created managers (which wrap
                some more complicated structure)
            theory_params : dict
                theory dictionary containing all needed parameters
    """

    def __init__(self, obs_name, runner=None, *, eko_components, theory_params, obs_params):
        # internal managers
        self.obs_name = obs_name
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
        self.FONLL_damping = theory_params["FONLL_damping"]
        self.damping_powers = theory_params["damping_powers"]
        self.obs_params = obs_params

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
            self.__ESFs.append(self.get_esf(self.obs_name, kinematics, use_raw=False))

    def get_esf(self, obs_name, kinematics, *args, use_raw=True, force_local=False):
        """
            Returns a :py:class:`EvaluatedStructureFunction` instance.

            This wrappers allows

            - TMC to to access raw computations
            - heavy quark matching schemes to access their light counter parts

            It also implements an internal caching system, to speed up the integrals
            in TMC.

            Parameters
            ----------
                obs_name : .observable_name.ObservableName
                    structure function name
                kinematics : dict
                    kinematic configuration
                args : any
                    further arguments passed down to the instance
                use_raw : bool
                    eventually use the ESFTMC? (or just the uncorrected one)

            Returns
            -------
                obj : EvaluatedStructureFunction
                    created object
        """
        # if force_local is active suppress caching to avoid circular dependecy
        if force_local:
            obj = ESFmap[obs_name.flavor_family](self, kinematics, force_local=True)
            return obj
        # else we're happy to cache
        # is it us or do we need to delegate?
        if obs_name == self.obs_name:
            # convert to tuple
            key = list(kinematics.values())
            use_tmc_if_available = not use_raw and self.TMC != 0
            key.append(use_tmc_if_available)
            key = tuple(key)
            # TODO how to incorporate args?
            # search
            try:
                return self.__ESFcache[key]
            except KeyError:
                if use_tmc_if_available:
                    obj = ESFTMCmap[obs_name.kind](self, kinematics)
                else:
                    obj = ESFmap[obs_name.flavor_family](self, kinematics, *args)
                self.__ESFcache[key] = obj
                return obj
        else:
            # ask our parent (as always)
            return self.__runner.observable_instances[obs_name.name].get_esf(
                obs_name, kinematics, *args
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
