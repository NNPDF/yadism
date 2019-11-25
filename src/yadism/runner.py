# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""

from yadism.structure_functions import f2_LO
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
    charges = [-1 / 3, 2 / 3] * 3
    sq_charge_av = sum(charges[:n_f]) / n_f

    # compute input grid
    is_log_interpolation = setup.get("is_log_interpolation", True)
    if is_log_interpolation:
        get_fnc = get_Lagrange_basis_functions
    else:
        get_fnc = get_Lagrange_basis_functions_log
    xgrid = setup["xgrid"]
    coeffs = get_fnc(xgrid, setup["polynom_rank"])

    ret = {"xgrid": xgrid}

    # iterate polynoms
    f2_res = []
    for j, coeff in enumerate(coeffs):
        elem = {}
        # iterate processes
        if setup["process"] == "F2":
            pref_f2_singlet = x * sq_charge_av * setup["alphaqed"]
            f2_res.append(pref_f2_singlet * f2_LO(x, Q2, coeff, is_log_interpolation))
    ret["F2"] = f2_res
    # TODO implement all other processes: FL, sigma, ?
    return ret
