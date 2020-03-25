# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""
import copy

import numpy as np

from eko.interpolation import InterpolatorDispatcher
from yadism.structure_functions.LO import f2_light_LO_quark


def get_configurations(observable, sq_charge_av):
    def singlet(x: float, Q2: float, polynom_f) -> float:
        pref_f2_singlet = x
        return pref_f2_singlet * f2_light_LO_quark(x, Q2, polynom_f)

    def gluon(x: float, Q2: float, polynom_coeff: dict) -> float:
        return None

    def nonsinglet(x: float, Q2: float, polynom_coeff: dict) -> float:
        return None

    return [("S", singlet), ("g", None), ("NS", None)]


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

    # compute charge factors
    charges = np.array([-1 / 3, 2 / 3] * 3)
    sq_charge_av = np.average(charges[:n_f] ** 2)

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
    empty = np.zeros(len(xgrid))
    output_vectors = dict(S=empty.copy(), NS=empty.copy(), g=empty.copy())
    for obs in ["F2", "FL"]:
        if obs in dis_observables:
            output = {**output, obs: []}
            for kinematics in dis_observables[obs]:
                if 1 < kinematics["x"] < 0:
                    raise ValueError("Kinematics 'x' must be in the range (0,1)")
                if kinematics["Q2"] < 0:
                    raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")
                output[obs].append({**kinematics, **copy.deepcopy(output_vectors)})

    # iterate all polynomials
    for c, poly_f in enumerate(interpolator):
        # iterate F2 configurations
        for k, kinematics in enumerate(dis_observables.get("F2", [])):
            # iterate contributions
            for key, f in get_configurations("F2", sq_charge_av):
                # skip zeros
                if None == f:
                    continue
                output["F2"][k][key][c] = f(kinematics["x"], kinematics["Q2"], poly_f)

    # TODO implement all other processes: FL, sigma, ?
    return output
