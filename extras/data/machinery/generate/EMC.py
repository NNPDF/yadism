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
    "emc_c_d": ["EMC_90_NC_C_D_F2_NUM", "EMC_90_NC_C_D_F2_DEN"],
    "emc_ca_d": ["EMC_90_NC_Ca_D_F2_NUM", "EMC_90_NC_Ca_D_F2_DEN"],
    "emc_cu_d": ["EMC_93_NC_Cu_D_F2_NUM", "EMC_93_NC_Cu_D_F2_DEN"],
    "emc_fe_d": ["EMC_97_NC_Fe_D_F2_NUM", "EMC_97_NC_Fe_D_F2_DEN"],
    "emc_sn_d": ["EMC_88_NC_Sn_D_F2_NUM", "EMC_88_NC_Sn_D_F2_DEN"],
}
