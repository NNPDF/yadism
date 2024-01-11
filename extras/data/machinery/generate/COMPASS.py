from .utils import load, obs_template
def dump(src_path, _target):
    '''Generate the input card for COMPASS measurements.

    Parameters
    ----------
    src_path : str
        input path

    Returns
    -------
    dict
        observables dictionary, corresponding to the runcard

    '''
    obs = obs_template.copy()
    data = load(src_path, 0, ["x", "Q2"])
    dict_kins = [
        dict(x=d["x"]["mid"], y=d["y"]["mid"], Q2=d["Q2"]["mid"])
        for d in data
    ]

    # Details regarding the observables
    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"
    obs["PolarizationDIS"] = 1.0
    obs["TargetDIS"] = "proton"
    obs["observables"] = {"g1_total": dict_kins}

    return obs


# renaming
new_names = {
    "compass_g1": "COMPASS_NC_17GEV_MUP",
}
