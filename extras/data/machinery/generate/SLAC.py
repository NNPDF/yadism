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
    obs = obs_template.copy()
    data = load(src_path, 0, ["x", "Q2"])
    esf = [dict(x=d["x"], y=1.0, Q2=d["Q2"]) for d in data]
    obs["prDIS"] = "NC"
    obs["observables"] = {"F2_total": esf}
    obs["ProjectileDIS"] = "electron"
    # Make sure that the nuclear datasets are computed with a `proton`
    # target even if we have `Deuteron` in the denominator.
    obs["TargetDIS"] = "isoscalar" if "_D_" in target.parent.name else "proton"

    return obs


# renaming
new_names = {
    "slac_d": "SLAC_NC_EM_D_F2",
    "slac_p": "SLAC_NC_EM_P_F2",
    "slac_he_d": "SLACE139_HE_D",
}
