# -*- coding: utf-8 -*-
"""
Defines the :py:class:`StructureFunction` class.

.. todo::
    refer to the sf-esf overview
"""
import logging

from .esf import esf
from .tmc import ESFTMCmap

logger = logging.getLogger(__name__)


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

    def __init__(self, obs_name, runner):
        # internal managers
        self.obs_name = obs_name
        self.runner = runner
        self.__ESFs = []
        self.__ESFcache = {}
        logger.debug("Init %s", self)

    def __getattribute__(self, name):
        runner = object.__getattribute__(self, "runner")
        if name in runner.managers:
            return runner.managers[name]
        if name in runner.theory_params:
            return runner.theory_params[name]
        return super().__getattribute__(name)

    def __repr__(self):
        return self.obs_name.name

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
            obj = esf.EvaluatedStructureFunction(self, kinematics)
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
                    obj = esf.EvaluatedStructureFunction(self, kinematics, *args)
                self.__ESFcache[key] = obj
                return obj
        else:
            # ask our parent (as always)
            if obs_name.name not in self.runner.observable_instances:
                self.runner.observable_instances[obs_name.name] = type(self)(
                    obs_name, self.runner
                )
            return self.runner.observable_instances[obs_name.name].get_esf(
                obs_name, kinematics, *args
            )

    def get_result(self):
        """
        Collects the results from all childrens.

        Returns
        -------
            output : list(ESFResult)
                all children outputs
        """
        output = []
        for esf in self.__ESFs:
            output.append(esf.get_result())

        return output
