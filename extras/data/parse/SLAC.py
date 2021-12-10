from .utils import load, obs_template


def dump(src_path):
    """
    Compute SLAC observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    data = load(src_path, 0, ["x", "Q2"])
    esf = [dict(x=d["x"], y=1.0, Q2=d["Q2"]) for d in data]
    obs["prDIS"] = "NC"
    obs["observables"] = {"F2total": esf}
    obs["ProjectileDIS"] = "electron"
    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "slac_d": "SLAC_NC_EM_D_F2",
    "slac_p": "SLAC_NC_EM_P_F2",
}
