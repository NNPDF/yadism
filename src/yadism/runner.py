# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""

import numpy as np

from eko.interpolation import InterpolatorDispatcher

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
    """

    def __init__(self, theory, dis_observables):
        self._theory = theory
        self._dis_observables = dis_observables
        self._n_f = theory["NfFF"]

        polynomial_degree = dis_observables["polynomial_degree"]
        self._interpolator = InterpolatorDispatcher(
            dis_observables["xgrid"],
            polynomial_degree,
            log=dis_observables.get("is_log_interpolation", True),
            mode_N=False,
        )

        self.f2 = F2(self._interpolator)
        self.fL = FL(self._interpolator)

        self._output = Output()
        self._output["xgrid"] = self._interpolator.xgrid

        self.f2.load(self._dis_observables.get("F2", []))
        self.fL.load(self._dis_observables.get("FL", []))

    def get_output(self):
        self._output["F2"] = self.f2.get_output()
        self._output["FL"] = self.fL.get_output()

        return self._output

    def __call__(self, pdfs):
        """
        Returns
        -------
        dict
            dictionary with all computed processes

        """

        output = self.get_output()

        def get_charged_sum(z, Q2):
            """Short summary.

            d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9
            """
            pdf_fl = lambda k: pdfs.xfxQ2(k, z, Q2)  # / x
            return (pdf_fl(1) + pdf_fl(-1) + pdf_fl(3) + pdf_fl(-3)) / 9 + (
                pdf_fl(2) + pdf_fl(-2)
            ) * 4 / 9

        ret = {"F2": []}
        for kin in output["F2"]:
            # collect pdfs
            fq = []
            for z in self._interpolator.xgrid:
                fq.append(get_charged_sum(z, kin["Q2"]))

            # contract with coefficient functions
            result = np.dot(fq, kin["q"])
            ret["F2"].append(dict(x=kin["x"], Q2=kin["Q2"], result=result))

        return ret

    def apply(self, pdfs):
        return self(pdfs)

    def clear(self):
        "Or 'restart' or whatever"
        pass

    def dump(self):
        "If any output available ('computed') dump the current output on file"
        pass


def run_dis(theory: dict, dis_observables: dict) -> dict:
    runner = Runner(theory, dis_observables)
    return runner
