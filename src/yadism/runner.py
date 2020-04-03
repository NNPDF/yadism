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
from .structure_functions import F2, FL


class Runner:
    """Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution.
    dis_observables : dict
        DIS parameters: process description, kinematic specification for the
        requested output.

    .. todo::
        * reference on theory template
        * detailed description of dis_observables entries
    """

    def __init__(self, theory: dict, dis_observables: dict):
        # ============
        # Store inputs
        # ============
        self._theory = theory
        self._dis_observables = dis_observables
        self._n_f: int = theory["NfFF"]

        # ===========================
        # Setup interpolator from eko
        # ===========================
        polynomial_degree: int = dis_observables["polynomial_degree"]
        self._interpolator = InterpolatorDispatcher(
            dis_observables["xgrid"],
            polynomial_degree,
            log=dis_observables.get("is_log_interpolation", True),
            mode_N=False,
        )

        # ==========================
        # Create physics environment
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

        self._pto = theory["PTO"]

        # ==============================
        # Initialize structure functions
        # ==============================
        self.f2 = F2(
            interpolator=self._interpolator,
            constants=self._constants,
            threshold=self._threshold,
            alpha_s=self._alpha_s,
            pto=self._pto,
        )
        self.fL = FL(
            interpolator=self._interpolator,
            constants=self._constants,
            threshold=self._threshold,
            alpha_s=self._alpha_s,
            pto=self._pto,
        )

        # =================
        # Initialize output
        # =================
        self._output = Output()
        self._output["xgrid"] = self._interpolator.xgrid

        # ===============================================
        # Load process description in structure functions
        # ===============================================
        self.f2.load(self._dis_observables.get("F2", []))
        self.fL.load(self._dis_observables.get("FL", []))

    def get_output(self) -> Output:
        """
            Compute coefficient functions grid for requested kinematic points.


            .. admonition:: Implementation Note

                get_output pipeline

            Returns
            -------
            Output
                output object, it will store the coefficient functions grid
                (flavour, interpolation-index) for each requested kinematic
                point (x, Q2)


            .. todo::

                * docs
                * get_output pipeline
        """
        self._output["F2"] = self.f2.get_output()
        self._output["FL"] = self.fL.get_output()

        return self._output

    def __call__(self, pdfs: Any) -> dict:
        """
            __call__.

            Parameters
            ----------
            pdfs : Any
                pdfs

            Returns
            -------
            dict

            .. todo::
                docs
        """
        # init output
        output = self.get_output()

        def get_charged_sum(z: float, Q2: float) -> float:
            """
                Compute charged sum of PDF at :math:`(x, Q^2)`.

                For 3 flavors:
                .. math::
                    d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9
                For n flavors (missing):
                .. math::
                    \sum_f Q_f^2 (q_f(x, Q^2) + \\bar(q)_f(x, Q^2))
            """
            # preload (z, Q2)
            pdf_fl = lambda k: pdfs.xfxQ2(k, z, Q2)
            # compute and return the sum
            return (pdf_fl(1) + pdf_fl(-1) + pdf_fl(3) + pdf_fl(-3)) / 9 + (
                pdf_fl(2) + pdf_fl(-2)
            ) * 4 / 9

        # init return dict
        ret: dict = {"F2": [], "FL": []}

        for sf in ["F2", "FL"]:  # loop over structure functions
            for kin in output[sf]:  # loop over kinematic points (x, Q2)
                # collect pdfs
                fq = []
                fg = []
                for z in self._interpolator.xgrid_raw:
                    fq.append(get_charged_sum(z, kin["Q2"]) / z)
                    fg.append(pdfs.xfxQ2(21, z, kin["Q2"]) / z)

                # contract with coefficient functions
                result = kin["x"] * (
                    np.dot(fq, kin["q"]) + 2 / 9 * np.dot(fg, kin["g"])
                )
                # store the result
                ret[sf].append(dict(x=kin["x"], Q2=kin["Q2"], result=result))

        return ret

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
        pass

    def dump(self) -> None:
        """
        If any output available ('computed') dump the current output on file

        .. todo::
            - implement
            - docs
        """
        pass


def run_dis(theory: dict, dis_observables: dict) -> Runner:
    """
        run_dis.

        Parameters
        ----------
        theory : dict
            theory
        dis_observables : dict
            dis_observables

        Returns
        -------
        Runner

        .. todo::
            - decide the purpose
            - implement
            - docs
    """
    runner = Runner(theory, dis_observables)
    return runner
