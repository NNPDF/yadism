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
    if "alphaqed" in new_theory:
        new_theory["alphaem"] = new_theory.pop("alphaqed")
    # TODO: update Yadism syntax and remove PTO everywhere?
    if "QED" in new_theory:
        new_theory["order"] = (new_theory["PTO"] + 1, new_theory.pop("QED"))
    return new_theory, new_obs


def update_scale_variations(theory):
    """
    Extract necessity to compute scale variations.

    Parameters
    ----------
        theory : dict
            theory runcard
    """
    if "RenScaleVar" not in theory:
        theory["RenScaleVar"] = not np.isclose(theory["XIR"], 1.0)
    if "FactScaleVar" not in theory:
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
    elif target == "neon":
        obs["TargetDIS"] = {"Z": 10.0, "A": 20.0}
        obs["TargetDISid"] = "1000100200"
    elif target == "marble":
        A = (40 + 3 * 16 + 12) / 5  # A(CaCO3): average atomic mass
        Z = (20 + 3 * 8 + 6) / 5  # Z(CaCO3): avaerage atomic number
        obs["TargetDIS"] = {"Z": Z, "A": A}
        obs["TargetDISid"] = f"1000{str(Z)}{str(A)}0"
    else:
        raise ValueError(f"Unknown TargetDIS '{target}'")


def update_fns(theory):
    """
    Sets k{fl}Thr and  ZM{fl} for all heavy flavours depending on the scheme.

    Parameters
    ----------
        theory : dict
            theory runcard
    """
    fns = theory["FNS"]
    nf = theory["NfFF"]

    if fns == "ZM-VFNS":
        for fl in hqfl:
            theory[f"ZM{fl}"] = True
    elif "FONLL" in fns:
        # enforce correct settings moving all thresholds to 0 or oo
        for k, fl in enumerate(hqfl):
            if k + 4 <= nf:
                theory[f"k{fl}Thr"] = 0.0
                theory[f"ZM{fl}"] = True
            elif k + 4 > nf + 1:
                theory[f"k{fl}Thr"] = np.inf
                theory[f"ZM{fl}"] = True
            else:
                # We only consider a single massive contribution. This is to
                # prevent double counting when different FNS are combined
                # to produce FONLL
                theory[f"k{fl}Thr"] = np.inf
                theory[f"ZM{fl}"] = False
    elif "FFN" in fns:
        # enforce correct settings moving all thresholds to 0 or oo
        for k, fl in enumerate(hqfl):
            if k + 4 <= nf:
                theory[f"k{fl}Thr"] = 0.0
                theory[f"ZM{fl}"] = True
            else:
                # for these flavours the massive contribution is calculated,
                # but they do not contribute to the number of running flavors
                theory[f"k{fl}Thr"] = np.inf
                theory[f"ZM{fl}"] = False
    else:
        raise ValueError(f"Scheme '{fns}' not recognized.")

    if "PTODIS" not in theory:
        theory["PTODIS"] = theory["PTO"]

    if "FONLLParts" not in theory:
        theory["FONLLParts"] = "full"
