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
import time

from eko.interpolation import InterpolatorDispatcher
from eko.constants import Constants
from eko import thresholds
from eko import strong_coupling

from .output import Output
from .sf import StructureFunction as SF
from .structure_functions import ESFmap
from .coupling_constants import CouplingConstants
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

        # ===========================
        # Setup eko stuff
        # ===========================
        self.interpolator = InterpolatorDispatcher.from_dict(
            observables, mode_N=False, numba_it=False
        )
        self.constants = Constants()
        self.threshold = thresholds.ThresholdsConfig.from_dict(theory)
        self.strong_coupling = strong_coupling.StrongCoupling.from_dict(
            theory, self.threshold, self.constants
        )

        # Non-eko theory
        self.coupling_constants = CouplingConstants.from_theory(theory)
        self.xiF = theory["XIF"]

        # ==============================
        # Initialize structure functions
        # ==============================
        eko_components = dict(
            interpolator=self.interpolator,
            constants=self.constants,
            threshold=self.threshold,
            alpha_s=self.strong_coupling,
            coupling_constants=self.coupling_constants,
        )
        # FONLL damping powers
        FONLL_damping = bool(theory["DAMP"])
        if FONLL_damping:
            damping_power = theory.get("DAMPPOWER", 2)
            damping_power_c = theory.get("DAMPPOWERCHARM", damping_power)
            damping_power_b = theory.get("DAMPPOWERBOTTOM", damping_power)
            damping_power_t = theory.get("DAMPPOWERTOP", damping_power)
            damping_powers = [damping_power_c, damping_power_b, damping_power_t]
        else:
            damping_powers = [2] * 3
        # pass theory params
        theory_params = dict(
            pto=theory["PTO"],
            xiR=theory["XIR"],
            xiF=self.xiF,
            M2hq=None,
            TMC=theory["TMC"],
            M2target=theory["MP"] ** 2,
            FONLL_damping=FONLL_damping,
            damping_powers=damping_powers,
        )

        self.observable_instances = {}
        for name in ESFmap:
            lab = utils.get_mass_label(name)
            if lab is not None:
                theory_params["M2hq"] = theory[lab] ** 2

            # initialize an SF instance for each possible structure function
            obj = SF(
                name,
                runner=self,
                eko_components=eko_components,
                theory_params=theory_params,
            )

            # read kinematics
            obj.load(self._observables.get(name, []))
            self.observable_instances[name] = obj

        # =================
        # Initialize output
        # =================
        self._output = Output()
        self._output["xgrid"] = self.interpolator.xgrid_raw.tolist()
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
        start = time.time()
        for name, obs in self.observable_instances.items():
            if name in self._observables.keys():
                self._output[name] = obs.get_output()
        end = time.time()
        diff = end - start
        # TODO move to log and make more readable
        print(f"took {diff:.2f} s")

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
