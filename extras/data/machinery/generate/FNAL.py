
# -*- coding: utf-8 -*-
from .utils import load, obs_template


def dump(src_path, target):
    """Compute SLAC observables.

    Parameters
    ----------
    src_path : str
        input path

    Returns
    -------
    dict
        observables dictionary, corresponding to the runcard

    """
    del target

    obs = obs_template.copy()
    data = load(src_path, 0, ["-", "x", "Q2", "y"])
    esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]

    obs["prDIS"] = "NC"
    obs["observables"] = {"F2_total": esf}
    obs["ProjectileDIS"] = "electron"

    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "fnal_c_d": "FNALE665_C_D",
    "fnal_ca_d": "FNALE665_Ca_D",
    "fnal_pdb_d": "FNALE665_Pb_D",
    "fnal_xe_d": "FNALE665_Xe_D",
}
