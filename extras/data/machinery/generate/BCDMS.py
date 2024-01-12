import pathlib
import tempfile

from .utils import load, obs_template, check_duplicate_kins


def dump(src_path, _target):
    """Compute BCDMS observables.

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

    esf = []
    if "bcd_" in src.stem:  # Proton Dataset
        text = src.read_text()
        with tempfile.NamedTemporaryFile(mode="w") as ntf:
            cut_text = "\n".join(text.splitlines()[::2])
            ntf.write(cut_text)
            ntf.flush()
            data = load(ntf.name, 0, ["x", "y", "Q2"])
            esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
    else:
        data = load(str(src), 0, ["-", "x", "Q2", "y"])
        esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]

    check_duplicate_kins(esf, subset=["x", "Q2"])

    obs["prDIS"] = "NC"
    obs["observables"] = {"F2_total": esf}
    obs["ProjectileDIS"] = "electron"

    if "bcd_d" in src.stem:
        obs["TargetDIS"] = "isoscalar"
    else:
        obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "bcd_d120": ["BCDMS_NC_100GEV_EM_D_F2", "BCDMS_NC_100GEV_D_F2"],
    "bcd_d200": ["BCDMS_NC_200GEV_EM_D_F2", "BCDMS_NC_200GEV_D_F2"],
    "bcd_d280": ["BCDMS_NC_280GEV_EM_D_F2", "BCDMS_NC_280GEV_D_F2"],
    "bcd_p100": "BCDMS_NC_100GEV_EM_P_F2",
    "bcd_p120": "BCDMS_NC_120GEV_EM_P_F2",
    "bcd_p200": "BCDMS_NC_200GEV_EM_P_F2",
    "bcd_p280": "BCDMS_NC_280GEV_EM_P_F2",
    "bcdms_fe_d": ["BCDMS_85_NC_Fe_D_F2_NUM", "BCDMS_85_NC_Fe_D_F2_DEN"],
    "bcdms_n_d": ["BCDMS_85_NC_N_D_F2_NUM", "BCDMS_85_NC_N_D_F2_DEN"],
}
