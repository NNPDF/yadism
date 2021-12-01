# -*- coding: utf-8 -*-
import warnings

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
    if "FONLL" not in fns:  # = fns in FFNS or ZM-VFNS
        # enforce correct settings moving all thresholds to 0 or oo
        if fns == "FFNS":
            ks = [0] * (nf - 3) + [np.inf] * (6 - nf)
            for k, fl in zip(ks, hqfl):
                theory[f"k{fl}Thr"] = k
        # here there is no difference between DGLAP and DIS
        for fl in hqfl:
            theory[f"kDIS{fl}Thr"] = theory[f"k{fl}Thr"]
    else:
        # keep the old setup for the ZM-VFNS part (above)
        for pid in range(nf + 1, 6 + 1):
            fl = hqfl[pid - 4]
            if f"kDIS{fl}Thr" in theory and not np.isclose(
                theory[f"kDIS{fl}Thr"], theory[f"k{fl}Thr"]
            ):
                warnings.warn(
                    f"kDIS{fl}Thr is not equal to k{fl}Thr in the given theory and"
                    f" is not the relevant FONLL threshold! kDIS{fl}Thr will be overwritten"
                )
            theory[f"kDIS{fl}Thr"] = theory[f"k{fl}Thr"]
        # for the actual value - keep it or fallback to evolution
        hfl = hqfl[nf - 4]
        if f"kDIS{hfl}Thr" not in theory:
            theory[f"kDIS{hfl}Thr"] = theory[f"k{hfl}Thr"]
        # erase all lower thresholds, meaning lower than the interesting one (NfFF)
        for pid in range(4, nf + 1):
            fl = hqfl[pid - 4]
            # we actually need to run in the nf-FNS so even kill that one
            theory[f"k{fl}Thr"] = 0
            if pid < nf:
                theory[f"kDIS{fl}Thr"] = 0
    # fix FONLL-B and introduce PTODIS
    if fns == "FONLL-B":
        theory["PTODIS"] = 2
        theory["PTO"] = 1
    else:
        theory["PTODIS"] = theory["PTO"]
