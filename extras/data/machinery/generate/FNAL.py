from .utils import check_duplicate_kins, load, obs_template


def dump(src_path, _target):
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
    data = load(src_path, 0, ["-", "x", "Q2", "y"])
    esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
    check_duplicate_kins(esf, subset=["x", "Q2"])

    obs["prDIS"] = "NC"
    obs["observables"] = {"F2_total": esf}
    obs["ProjectileDIS"] = "electron"

    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "fnal_c_d": ["FNAL_E665_NC_C_D_F2_NUM", "FNAL_E665_NC_C_D_F2_DEN"],
    "fnal_ca_d": ["FNAL_E665_NC_Ca_D_F2_NUM", "FNAL_E665_NC_Ca_D_F2_DEN"],
    "fnal_pb_d": ["FNAL_E665_NC_Pb_D_F2_NUM", "FNAL_E665_NC_Pb_D_F2_DEN"],
    "fnal_xe_d": ["FNAL_E665_NC_Xe_D_F2_NUM", "FNAL_E665_NC_Xe_D_F2_DEN"],
}
