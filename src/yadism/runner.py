# -*- coding: utf-8 -*-
"""
This module contains the main loop for the DIS calculations.

There are two ways of using ``yadism``:

* ``Runner``: this class provides a runner that get the *theory* and
  *observables* descriptions as input and manage the whole observables'
  calculation process
* ``run_dis``: a function that wraps the construction of a ``Runner`` object
  and calls the proper method to get the requested output

.. todo::
    decide about ``run_dis`` and document it properly in module header
"""
from typing import Any

import numpy as np

from eko.interpolation import InterpolatorDispatcher
from eko.constants import Constants
from eko.thresholds import Threshold
from eko.alpha_s import StrongCoupling

from .output import Output
from .sf import StructureFunction as SF
from .structure_functions import ESFmap
from . import utils


class Runner:
    """
        Wrapper to compute a process

        Parameters
        ----------
        theory : dict
            Dictionary with the theory parameters for the evolution (currently
            including PDFSet and DIS process indication).
        observables : dict
            DIS parameters: process description, kinematic specification for the
            requested output.

        Notes
        -----
        For a full description of the content of `theory` and `dis_observables`
        dictionaries read ??.

        .. todo::
            * reference on theory template
            * detailed description of dis_observables entries

    """

    def __init__(self, theory: dict, observables: dict):
        # ============
        # Store inputs
        # ============
        self._theory = theory
        self._observables = observables
        self._n_f: int = theory["NfFF"]

        # ===========================
        # Setup interpolator from eko
        # ===========================
        polynomial_degree: int = observables["polynomial_degree"]
        self.interpolator = InterpolatorDispatcher(
            observables["xgrid"],
            polynomial_degree,
            log=observables.get("is_log_interpolation", True),
            mode_N=False,
            numba_it=False,  # TODO: make it available for the user to choose
        )

        # ==========================
        # Create physics environment
        # ==========================
        self.constants = Constants()

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
        self.threshold = Threshold(
            q2_ref=q2_ref, scheme=FNS, threshold_list=threshold_list, nf=nf
        )

        # Now generate the operator alpha_s class
        alpha_ref = theory["alphas"]
        q2_alpha = pow(theory["Qref"], 2)
        self.strong_coupling = StrongCoupling(
            self.constants, alpha_ref, q2_alpha, self.threshold
        )

        self.xiF = theory["XIF"]

        # ==============================
        # Initialize structure functions
        # ==============================
        eko_components = dict(
            interpolator=self.interpolator,
            constants=self.constants,
            threshold=self.threshold,
            alpha_s=self.strong_coupling,
        )
        theory_stuffs = dict(
            pto=theory["PTO"],
            xiR=theory["XIR"],
            xiF=self.xiF,
            M2hq=None,
            TMC=theory["TMC"],
            M2target=theory["MP"] ** 2,
        )

        self.observable_instances = {}
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
            self.observable_instances[name] = obj

        # =================
        # Initialize output
        # =================
        self._output = Output()
        self._output["xgrid"] = self.interpolator.xgrid_raw
        self._output["xiF"] = self.xiF

    def get_output(self) -> Output:
        """
            Compute coefficient functions grid for requested kinematic points.


            .. admonition:: Implementation Note

                get_output pipeline

            Returns
            -------
            :obj:`Output`
                output object, it will store the coefficient functions grid
                (flavour, interpolation-index) for each requested kinematic
                point (x, Q2)


            .. todo::

                * docs
                * get_output pipeline
        """
        for name, obs in self.observable_instances.items():
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

        return self.get_output().apply_pdf(pdfs)

    def apply(self, pdfs: Any) -> dict:
        """
        Alias for the `__call__` method.

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

    def dump(self) -> None:
        """
        If any output available ('computed') dump the current output on file

        .. todo::
            - implement
            - docs
        """
        return self.get_output().dump()
