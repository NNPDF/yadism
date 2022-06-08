# -*- coding: utf-8 -*-
import logging

from .esf import exs

logger = logging.getLogger(__name__)


class CrossSection:
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
        self.exss = []
        logger.debug("Init %s", self)

    def __repr__(self):
        return self.obs_name.name

    def __len__(self):
        return len(self.exss)

    @property
    def elements(self):
        return self.exss

    def load(self, kinematic_configs):
        """
        Loads all kinematic configurations from the run card.

        Parameters
        ----------
            kinematic_configs : list(dict)
                run card input
        """
        self.exss = []
        for kinematics in kinematic_configs:
            self.exss.append(
                exs.EvaluatedCrossSection(
                    kinematics, self.obs_name, self.runner.configs, self.get_esf
                )
            )

    def get_esf(self, obs_name, kin):
        return self.runner.get_sf(obs_name).get_esf(obs_name, kin, use_raw=False)

    def get_result(self):
        """
        Collects the results from all childrens.

        Returns
        -------
            output : list(ESFResult)
                all children outputs
        """
        return list(elem.get_result() for elem in self.elements)
