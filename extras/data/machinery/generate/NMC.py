import pathlib
import tempfile

from .utils import check_duplicate_kins, load, obs_template


def dump(src_path, target):
    """Compute NMC observables.

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
    src = pathlib.Path(src_path)

    if src.stem == "nmc_p":
        esf = []
        for sub in sorted(src.glob("*")):
            text = sub.read_text()
            with tempfile.NamedTemporaryFile(mode="w") as ntf:
                cut_text = "\n".join(text.splitlines())
                ntf.write(cut_text)
                ntf.flush()
                data = load(ntf.name, 0, ["x", "Q2", "y"])
                esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
        obs["observables"] = {"XSHERANC": esf}
        obs["TargetDIS"] = "proton"
    else:
        if len(src.stem.split("_")) == 3:
            data = load(str(src), 0, ["-", "x", "Q2", "y"])
            esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
        else:
            data = load(str(src), 0, ["x", "Q2"])
            esf = [dict(x=d["x"], y=1.0, Q2=d["Q2"]) for d in data]

        obs["observables"] = {"F2_total": esf}
        obs["TargetDIS"] = "isoscalar" if "_D_" in target.parent.name else "proton"

    # TODO: check the `y`-dimension should not be required here?
    check_duplicate_kins(esf, subset=["x", "Q2", "y"])

    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"

    return obs


# renaming
new_names = {
    "nmc_p": "NMC_NC_EM_P_SIGMARED",
    "nmc_f2df2p": [
        "NMC_NC_EM_P_F2",
        "NMC_NC_EM_D_F2",
        "NMC_p_D",
        "NMC_NC_D_P_F2_NUM",
        "NMC_NC_D_P_F2_DEN",
    ],
    "nmc_al_c": ["NCM_96_NC_Al_C_F2_NUM", "NCM_96_NC_Al_C_F2_DEN"],
    "nmc_be_c": ["NCM_96_NC_Be_C_F2_NUM", "NCM_96_NC_Be_C_F2_DEN"],
    "nmc_c_d": ["NCM_95_NC_C_D_F2_NUM", "NCM_95_NC_C_D_F2_DEN"],
    "nmc_c_li": ["NCM_96RE_NC_C_Li_F3_NUM", "NCM_96RE_NC_C_Li_F3_DEN"],
    "nmc_ca_c": ["NCM_96_NC_Ca_C_F2_NUM", "NCM_96_NC_Ca_C_F2_DEN"],
    "nmc_ca_d": ["NCM_95RE_NC_Ca_D_F2_NUM", "NCM_95RE_NC_Ca_D_F2_DEN"],
    "nmc_ca_li": ["NCM_96RE_NC_Ca_Li_F2_NUM", "NCM_96RE_NC_Ca_Li_F2_DEN"],
    "nmc_fe_c": ["NCM_96_NC_Fe_C_F2_NUM", "NCM_96_NC_Fe_C_F2_DEN"],
    "nmc_he_d": ["NCM_95RE_NC_He_D_F2_NUM", "NCM_95RE_NC_He_D_F2_DEN"],
    "nmc_li_d": ["NCM_95_NC_Li_D_F2_NUM", "NCM_95_NC_Li_D_F2_DEN"],
    "nmc_pb_c": ["NCM_96_NC_Pb_C_F2_NUM", "NCM_96_NC_Pb_C_F2_DEN"],
    "nmc_sn_c": ["NCM_96_NC_Sn_C_F2_NUM", "NCM_96_NC_Sn_C_F2_DEN"],
}
