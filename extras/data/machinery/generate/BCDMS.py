import pathlib
import tempfile

from .utils import load, obs_template


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
    text = src.read_text()
    with tempfile.NamedTemporaryFile(mode="w") as ntf:
        cut_text = "\n".join(text.splitlines()[::2])
        ntf.write(cut_text)
        ntf.flush()
        data = load(ntf.name, 0, ["x", "y", "Q2"])
        esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
    obs["prDIS"] = "NC"
    obs["observables"] = {"F2_total": esf}
    obs["ProjectileDIS"] = "electron"
    if "bcd_p" in src.stem:
        obs["TargetDIS"] = "proton"
    elif "bcd_d" in src.stem:
        obs["TargetDIS"] = "isoscalar"
    else:
        raise ValueError("BCDMS unknown data")

    return obs


# renaming
new_names = {
    "bcd_d120": "BCDMS_NC_100GEV_EM_D_F2",
    "bcd_d200": "BCDMS_NC_200GEV_EM_D_F2",
    "bcd_d280": "BCDMS_NC_280GEV_EM_D_F2",
    "bcd_p100": "BCDMS_NC_100GEV_EM_P_F2",
    "bcd_p120": "BCDMS_NC_120GEV_EM_P_F2",
    "bcd_p200": "BCDMS_NC_200GEV_EM_P_F2",
    "bcd_p280": "BCDMS_NC_280GEV_EM_P_F2",
}
