# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""
import numpy as np

from yadism.structure_functions import f2_light_LO
from yadism.interpolation import (
    get_Lagrange_basis_functions,
    get_Lagrange_basis_functions_log,
)


def run_dis(setup: dict) -> dict:
    """Wrapper to compute a process

    Parameters
    ----------
    setup : dict
        a dictionary with the theory parameters for the evolution

    Returns
    -------
    dict
        dictionary with all computed processes

    """
    # TODO sanity check
    # setup parameters
    x = setup["x"]
    Q2 = setup["Q2"]
    n_f = setup["NfFF"]

    # compute charge factors
    charges = np.array([-1 / 3, 2 / 3] * 3)
    sq_charge_av = np.average(charges[:n_f] ** 2)

    # compute input grid
    is_log_interpolation = setup.get("is_log_interpolation", True)
    if is_log_interpolation:
        get_fnc = get_Lagrange_basis_functions_log
    else:
        get_fnc = get_Lagrange_basis_functions
    xgrid = setup["xgrid"]
    coeffs = get_fnc(xgrid, setup["polynom_rank"])

    ret = {"xgrid": xgrid}

    # iterate polynoms
    if setup["process"] == "F2":
        f2_res = []
        pref_f2_singlet = x * sq_charge_av

    for coeff in coeffs:
        # iterate processes
        if setup["process"] == "F2":
            f2_res.append(
                pref_f2_singlet * f2_light_LO(x, Q2, coeff, is_log_interpolation)
            )

    if setup["process"] == "F2":
        ret["F2"] = np.array(f2_res)
    # TODO implement all other processes: FL, sigma, ?
    return ret
