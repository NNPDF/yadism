# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.
"""

from yadism.structure_functions import f2


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
    ret = {}
    # iterate processes
    if setup["process"] == "F2":
        ret["F2"] = f2(setup["x"], setup["Q2"])
    # TODO implement all other processes: FL, sigma, ?
    return ret
