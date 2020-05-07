# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.

.. todo::
    docs
"""
from typing import Any

import numpy as np

from eko.interpolation import InterpolatorDispatcher
from eko.constants import Constants
from eko.thresholds import Threshold
from eko.alpha_s import StrongCoupling

from .output import Output
from .StructureFunction import StructureFunction as SF
from .structure_functions import ESFmap
from . import utils


class Runner:
    """Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution.
    observables : dict
        Description of parameter `observables`.

    .. todo::
        docs
    """

    def __init__(self, theory: dict, observables: dict):
        self._theory = theory
        self._observables = observables
        self._n_f: int = theory["NfFF"]

        polynomial_degree: int = observables["polynomial_degree"]
        self._interpolator = InterpolatorDispatcher(
            observables["xgrid"],
            polynomial_degree,
            log=observables.get("is_log_interpolation", True),
            mode_N=False,
            numba_it=False,  # TODO: make it available for the user to choose
        )

        # ==========================
        # create physics environment
        # ==========================
        self._constants = Constants()

        FNS = theory["FNS"]
        q2_ref = pow(theory["Q0"], 2)
        if FNS != "FFNS":
            qmc = theory["Qmc"]
            qmb = theory["Qmb"]
            qmt = theory["Qmt"]
            threshold_list = pow(np.array([qmc, qmb, qmt]), 2)
            nf = None
        else:
            nf = theory["NfFF"]
            threshold_list = None
        self._threshold = Threshold(
            q2_ref=q2_ref, scheme=FNS, threshold_list=threshold_list, nf=nf
        )

        # Now generate the operator alpha_s class
        alpha_ref = theory["alphas"]
        q2_alpha = pow(theory["Qref"], 2)
        self._alpha_s = StrongCoupling(
            self._constants, alpha_ref, q2_alpha, self._threshold
        )

        self._xiF = theory["XIF"]

        # ==============================
        # initialize structure functions
        # ==============================
        eko_components = dict(
            interpolator=self._interpolator,
            constants=self._constants,
            threshold=self._threshold,
            alpha_s=self._alpha_s,
        )
        theory_stuffs = dict(
            pto=theory["PTO"],
            xiR=theory["XIR"],
            xiF=self._xiF,
            M2hq=None,
            TMC=theory["TMC"],
            M2target=theory["MP"]**2,
        )
        self._observable_instances = {}
        for name in ESFmap.keys():
            lab = utils.get_mass_label(name)
            if lab is not None:
                theory_stuffs["M2hq"] = theory[lab] ** 2

            # initialize an SF instance for each possible structure function
            obj = SF(
                name,
                runner=self,
                eko_components=eko_components,
                theory_stuffs=theory_stuffs,
            )

            # read kinematics
            obj.load(self._observables.get(name, []))
            self._observable_instances[name] = obj

        # prepare output
        self._output = Output()
        self._output["xgrid"] = self._interpolator.xgrid_raw
        self._output["xiF"] = self._xiF

    def get_output(self) -> Output:
        """
        .. todo::
            docs
        """
        for name, obs in self._observable_instances.items():
            if name in self._observables.keys():
                self._output[name] = obs.get_output()

        return self._output

    def __call__(self, pdfs: Any) -> dict:
        """
        Returns
        -------
        dict
            dictionary with all computed processes

        .. todo::
            docs
        """

        return self.get_output().apply_PDF(pdfs)

    def apply(self, pdfs: Any) -> dict:
        """
        .. todo::
            - implement
            - docs
        """
        return self(pdfs)

    def clear(self) -> None:
        """
        Or 'restart' or whatever

        .. todo::
            - implement
            - docs
        """
        pass

    def dump(self) -> None:
        """
        If any output available ('computed') dump the current output on file

        .. todo::
            - implement
            - docs
        """
        return self.get_output().dump()
