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
from .structure_functions import F2, FL


class Runner:
    """Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution.
    dis_observables : dict
        Description of parameter `dis_observables`.

    .. todo::
        docs
    """

    def __init__(self, theory: dict, dis_observables: dict):
        self._theory = theory
        self._dis_observables = dis_observables
        self._n_f: int = theory["NfFF"]

        polynomial_degree: int = dis_observables["polynomial_degree"]
        self._interpolator = InterpolatorDispatcher(
            dis_observables["xgrid"],
            polynomial_degree,
            log=dis_observables.get("is_log_interpolation", True),
            mode_N=False,
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

        self._pto = theory["PTO"]

        # ==============================
        # initialize structure functions
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

        self._output = Output()
        self._output["xgrid"] = self._interpolator.xgrid

        self.f2.load(self._dis_observables.get("F2", []))
        self.fL.load(self._dis_observables.get("FL", []))

    def get_output(self) -> Output:
        """
        .. todo::
            docs
        """
        self._output["F2"] = self.f2.get_output()
        self._output["FL"] = self.fL.get_output()

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

        output = self.get_output()

        def get_charged_sum(z: float, Q2: float) -> float:
            """Short summary.

            d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9

            .. todo::
                docs
            """
            pdf_fl = lambda k: pdfs.xfxQ2(k, z, Q2)  # / x
            return (pdf_fl(1) + pdf_fl(-1) + pdf_fl(3) + pdf_fl(-3)) / 9 + (
                pdf_fl(2) + pdf_fl(-2)
            ) * 4 / 9

        ret: dict = {"F2": []}
        for kin in output["F2"]:
            # collect pdfs
            fq = []
            fg = []
            for z in self._interpolator.xgrid:
                fq.append(get_charged_sum(z, kin["Q2"]))
                fg.append(pdfs.xfxQ2(21, z, kin["Q2"]))

            # contract with coefficient functions
            result = np.dot(fq, kin["q"]) + 2 / 9 * np.dot(fg, kin["g"])
            ret["F2"].append(dict(x=kin["x"], Q2=kin["Q2"], result=result))

        return ret

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
        pass


def run_dis(theory: dict, dis_observables: dict) -> Runner:
    """
    .. todo::
        - decide the purpose
        - implement
        - docs
    """
    runner = Runner(theory, dis_observables)
    return runner
