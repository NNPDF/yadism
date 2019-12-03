# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""
import numpy as np

from yadism.structure_functions.LO import f2_light_LO
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

    # GLOBAL

    # reading theory parameters
    # TODO sanity check (2 <= nf <= 6)
    n_f = setup["NfFF"]

    # compute charge factors
    charges = np.array([-1 / 3, 2 / 3] * 3)
    sq_charge_av = np.average(charges[:n_f] ** 2)

    # OBSERVABLES

    dis_observables = setup["dis_observables"]

    # compute input grid
    is_log_interpolation = dis_observables.get("is_log_interpolation", True)
    if is_log_interpolation:
        get_fnc = get_Lagrange_basis_functions_log
    else:
        get_fnc = get_Lagrange_basis_functions
    xgrid = dis_observables["xgrid"]
    coeffs = get_fnc(xgrid, dis_observables["polynom_rank"])

    # TODO sanity check (0 < x < 1, Q2 > 0)
    # setup parameters

    # prepare the output
    output = {"xgrid": xgrid}
    empty = np.zeros(len(coeffs))
    output_vectors = dict(S=empty.copy(), NS=empty.copy(), g=empty.copy())
    for obs in ["F2", "FL"]:
        if obs in dis_observables:
            output = {
                **output,
                obs: [
                    {**kinematics, **output_vectors}
                    for kinematics in dis_observables[obs]
                ],
            }

    # iterate all polynomials
    for c, coeff in enumerate(coeffs):
        # iterate F2 configurations
        for k, kinematics in enumerate(dis_observables.get("F2", [])):
            pref_f2_singlet = kinematics["x"] * sq_charge_av
            output["F2"][k]["S"][c] = pref_f2_singlet * f2_light_LO(
                kinematics["x"], kinematics["Q2"], coeff, is_log_interpolation
            )

    # TODO implement all other processes: FL, sigma, ?
    return output
