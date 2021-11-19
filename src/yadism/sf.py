# -*- coding: utf-8 -*-
"""
Defines the :py:class:`StructureFunction` class.

.. todo::
    refer to the sf-esf overview
"""
import logging

from .esf import esf, tmc

logger = logging.getLogger(__name__)


class StructureFunction:
    """
    Represents an abstract structure function.

    This class acts as an intermediate handler between the :py:class:`Runner`
    exposed to the outside and the :py:class:`EvaluatedStructureFunction`
    which compute the actual observable.

    Parameters
    ----------
        obs_name : ObservableName
            name
        runner : yadism.runner.Runner
            parent reference
    """

    def __init__(self, obs_name, runner):
        # internal managers
        self.obs_name = obs_name
        self.runner = runner
        self.esfs = []
        self.cache = {}
        logger.debug("Init %s", self)

    def __repr__(self):
        return self.obs_name.name

    def __len__(self):
        return len(self.esfs)

    def load(self, kinematic_configs):
        """
        Loads all kinematic configurations from the run card.

        Parameters
        ----------
            kinematic_configs : list(dict)
                run card input
        """
        self.esfs = []
        # iterate F* configurations
        for kinematics in kinematic_configs:
            self.esfs.append(self.get_esf(self.obs_name, kinematics, use_raw=False))

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
        # TODO rethink and refactor method - only used by TMC
        # TODO remove force_local
        # if force_local is active suppress caching to avoid circular dependecy
        if force_local:
            obj = esf.EvaluatedStructureFunction(
                kinematics, self.obs_name, self.runner.configs
            )
            return obj
        # else we're happy to cache
        # is it us or do we need to delegate?
        if obs_name == self.obs_name:
            # convert to tuple
            key = list(kinematics.values())
            use_tmc_if_available = not use_raw and self.runner.configs.TMC != 0
            key.append(use_tmc_if_available)
            key = tuple(key)
            # TODO how to incorporate args?
            # search
            try:
                return self.cache[key]
            except KeyError:
                if use_tmc_if_available:
                    obj = tmc.ESFTMCmap[obs_name.kind](self, kinematics)
                else:
                    obj = esf.EvaluatedStructureFunction(
                        kinematics, self.obs_name, self.runner.configs
                    )
                self.cache[key] = obj
                return obj
        else:
            # ask our parent (as always)
            return self.runner.get_sf(obs_name).get_esf(obs_name, kinematics, *args)

    def iterate_result(self):
        for owned_esf in self.esfs:
            yield owned_esf.get_result()

    def get_result(self):
        """
        Collects the results from all childrens.

        Returns
        -------
            output : list(ESFResult)
                all children outputs
        """
        return list(self.iterate_result())
