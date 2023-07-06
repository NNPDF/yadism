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

    if src.stem == "bcd_d" or src.stem == "bcd_p":
        esf = []
        for sub in sorted(src.glob("*")):
            text = sub.read_text()
            with tempfile.NamedTemporaryFile(mode="w") as ntf:
                cut_text = "\n".join(text.splitlines()[::2])
                ntf.write(cut_text)
                ntf.flush()
                data = load(ntf.name, 0, ["x", "y", "Q2"])
                esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
    else:
        data = load(str(src), 0, ["-", "x", "Q2", "y"])
        esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]

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
    "bcd_d": "BCDMS_NC_EM_D_F2",
    "bcd_p": "BCDMS_NC_EM_P_F2",
    "bcdms_fe_d": "BCDMS85_Fe_D",
    "bcdms_n_d": "BCDMS85_N_D",
    "bcdms_d": "BCDMS_D",
}
