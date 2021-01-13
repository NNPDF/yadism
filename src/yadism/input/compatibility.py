# -*- coding: utf-8 -*-
import numpy as np

hqfl = "cbt"


def update(theory):
    """
    Upgrade the legacy theory runcards with the new settings.

    Shifts kcThr around and add the kDIScThr parameter (likewise for all heavy quarks).

    Parameters
    ----------
        theory : dict
            theory run card

    Returns
    -------
        new_theory : dict
            upgraded theory run card
    """
    new_theory = theory.copy()
    fns = theory["FNS"]
    nf = theory["NfFF"]
    if fns not in ["FONLL-A"]:
        # enforce correct settings moving all thresholds to 0 or oo
        if fns == "FFNS":
            ks = [0] * (nf - 3) + [np.inf] * (6 - nf)
            for k, fl in zip(ks, hqfl):
                new_theory[f"k{fl}Thr"] = k
        # here there is no difference between DGLAP and DIS
        for fl in hqfl:
            new_theory[f"kDIS{fl}Thr"] = new_theory[f"k{fl}Thr"]
    else:
        # keep the old setup for the ZM-VFNS part (above)
        for fl in hqfl:
            new_theory[f"kDIS{fl}Thr"] = new_theory[f"k{fl}Thr"]
        for pid in range(4, nf + 1):
            fl = hqfl[pid - 4]
            new_theory[f"k{fl}Thr"] = 0
            # erase all lower thresholds, meaning lower than the interesting one (NfFF)
            if pid < nf:
                new_theory[f"kDIS{fl}Thr"] = 0
    return new_theory
