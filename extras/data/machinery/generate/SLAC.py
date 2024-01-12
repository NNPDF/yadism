from .utils import check_duplicate_kins, load, obs_template


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
    obs["TargetDIS"] = "isoscalar" if "_EM_D" in target.parent.name else "proton"
    print(f"**** {src_path}")
    check_duplicate_kins(esf, subset=["x", "Q2"])

    return obs


# renaming
new_names = {
    "slac_d": "SLAC_NC_EM_D_F2",
    "slac_p": "SLAC_NC_EM_P_F2",
    "slac_nuc_d": "SLAC_NC_D_F2",
    "slac_he_d": ["SLAC_E139_NC_He_D_F2_NUM", "SLAC_E139_NC_He_D_F2_DEN"],
    "slac_be_d": ["SLAC_E139_NC_Be_D_F2_NUM", "SLAC_E139_NC_Be_D_F2_DEN"],
    "slac_c_d": ["SLAC_E139_NC_C_D_F2_NUM", "SLAC_E139_NC_C_D_F2_DEN"],
    "slac_al_d": ["SLAC_E139_NC_Al_D_F2_NUM", "SLAC_E139_NC_Al_D_F2_DEN"],
    "slac_ca_d": ["SLAC_E139_NC_Ca_D_F2_NUM", "SLAC_E139_NC_Ca_D_F2_DEN"],
    "slac_fe_d": ["SLAC_E139_NC_Fe_D_F2_NUM", "SLAC_E139_NC_Fe_D_F2_DEN"],
    "slac_ag_d": ["SLAC_E139_NC_Ag_D_F2_NUM", "SLAC_E139_NC_Ag_D_F2_DEN"],
    "slac_au_d": ["SLAC_E139_NC_Au_D_F2_NUM", "SLAC_E139_NC_Au_D_F2_DEN"],
}
