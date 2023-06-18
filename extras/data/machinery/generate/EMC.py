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
    "emc_c_d": "EMC90_C_D",
    "emc_ca_d": "EMC90_Ca_D",
    "emc_cu_d": "EMC93_Cu_D",
    "emc_fe_d": "EMC97_Fe_D",
    "emc_sn_d": "EMC88_Sn_D",
}
