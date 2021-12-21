# -*- coding: utf-8 -*-

import numpy as np

hqfl = "cbt"


def update(theory, observables):
    """
    Upgrade the legacy theory and observable runcards with the new settings.

    Parameters
    ----------
        theory : dict
            theory runcard
        observables : dict
            observable runcard

    Returns
    -------
        new_theory : dict
            upgraded theory runcard
        new_obs : dict
            upgraded observable runcard
    """
    new_theory = theory.copy()
    new_obs = observables.copy()
    update_fns(new_theory)
    update_scale_variations(new_theory)
    update_target(new_obs)
    return new_theory, new_obs


def update_scale_variations(theory):
    """
    Extract necessity to compute scale variations.

    Parameters
    ----------
        theory : dict
            theory runcard
    """
    theory["RenScaleVar"] = not np.isclose(theory["XIR"], 1.0)
    theory["FactScaleVar"] = not np.isclose(theory["XIF"], 1.0)


def update_target(obs):
    """
    Map TargetDIS string to a (Z,A) dict.

    Parameters
    ----------
        obs : dict
            observable runcard
    """
    target = obs["TargetDIS"]
    if not isinstance(target, str):
        return
    if target == "proton":
        obs["TargetDIS"] = {"Z": 1.0, "A": 1.0}
        # proton = 2212
        obs["TargetDISid"] = "2212"
    elif target == "neutron":
        obs["TargetDIS"] = {"Z": 0.0, "A": 1.0}
        # neutron = 2112
        obs["TargetDISid"] = "2112"
    elif target == "isoscalar":
        obs["TargetDIS"] = {"Z": 1.0, "A": 2.0}
        # deuteron = 10 0 001 002 0
        obs["TargetDISid"] = "1000010020"
    elif target == "iron":
        obs["TargetDIS"] = {
            "Z": 23.403,
            "A": 49.618,
        }  # Fe=26 and we don't know how these factors got inside APFEL
        # iron = 10 0 026 056 0
        obs["TargetDISid"] = "1000260560"
    elif target == "lead":
        obs["TargetDIS"] = {"Z": 82.0, "A": 208.0}  # from hep-ex/0102049
        # lead = 10 0 082 208 0
        obs["TargetDISid"] = "1000822080"
    else:
        raise ValueError(f"Unknown TargetDIS '{target}'")


def update_fns(theory):
    """
    Shifts kcThr around and add the kDIScThr parameter (likewise for all heavy quarks).

    Parameters
    ----------
        theory : dict
            theory runcard
    """
    fns = theory["FNS"]
    nf = theory["NfFF"]

    if "FONLL" in fns:
        theory["ZMc"] = False
        theory["ZMb"] = False
        theory["ZMt"] = True
    elif fns == "ZM-VFNS":
        for fl in hqfl:
            theory[f"ZM{fl}"] = True
    elif "FFNS" in fns:
        # enforce correct settings moving all thresholds to 0 or oo
        for k, fl in enumerate(hqfl):
            if k + 4 <= nf:
                theory[f"k{fl}Thr"] = 0.0
                theory[f"ZM{fl}"] = True
            else:
                theory[f"k{fl}Thr"] = np.inf
                theory[f"ZM{fl}"] = False
    else:
        raise ValueError(f"Scheme '{fns}' not recognized.")

    # here there is no difference between DGLAP and DIS
    for fl in hqfl:
        theory[f"kDIS{fl}Thr"] = theory[f"k{fl}Thr"]
