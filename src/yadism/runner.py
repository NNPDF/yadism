# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""
import copy

import numpy as np

from eko.interpolation import InterpolatorDispatcher
from yadism.structure_functions import F2, FL


def run_dis(theory: dict, dis_observables: dict) -> dict:
    """Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution.
    dis_observables : dict
        Description of parameter `dis_observables`.

    Returns
    -------
    dict
        dictionary with all computed processes

    """

    # GLOBAL

    # reading theory parameters
    n_f = theory["NfFF"]

    # OBSERVABLES

    # compute input grid
    is_log_interpolation = dis_observables.get("is_log_interpolation", True)
    xgrid = dis_observables["xgrid"]
    polynomial_degree = 2
    interpolator = InterpolatorDispatcher(
        xgrid, polynomial_degree, is_log_interpolation, mode_N=False
    )

    # setup parameters

    # prepare the output
    output = {"xgrid": xgrid}

    f2 = F2(interpolator)
    fL = FL(interpolator)

    f2.load(dis_observables.get("F2", []))
    fL.load(dis_observables.get("FL", []))
    # iterate contributions
    f2.compute()
    fL.compute()

    output["F2"] = f2.get_output()
    output["FL"] = fL.get_output()

    return output
