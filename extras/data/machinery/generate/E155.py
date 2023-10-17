from .utils import load, obs_template


def dump(src_path, target):
    """Generate the input card for E155 measurements.

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
    dict_kins = [
        dict(x=d["x"]["mid"], y=d["y"]["mid"], Q2=d["Q2"]["mid"]) for d in data
    ]
    # Details regarding the observables
    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"

    # if "_f1_" in str(src_path.stem):
    obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
    observable_name = "F1_total" if "_F1" in target.parent.name else "g1_total"
    obs["observables"] = {observable_name: dict_kins}
    if "_ep_" in str(src_path.stem):
        obs["TargetDIS"] = "proton"
    elif "_en_" in str(src_path.stem):
        obs["TargetDIS"] = "neutron"

    return obs


# renaming
new_names = {
    "e155_ep_g1f1": ["E155_NC_9GEV_EP_G1", "E155_NC_9GEV_EP_F1"],
    "e155_en_g1f1": ["E155_NC_9GEV_EN_G1", "E155_NC_9GEV_EN_F1"],
}
