import pathlib
import tempfile

from .utils import load, obs_template


def dump(src_path):
    """
    Compute BCDMS observables.

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
    for sub in src.glob("*"):
        text = sub.read_text()
        with tempfile.NamedTemporaryFile(mode="w") as ntf:
            cut_text = "\n".join(text.splitlines()[::2])
            ntf.write(cut_text)
            ntf.flush()
            data = load(ntf.name, 0, ["x", "y", "Q2"])
            esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]

    obs["prDIS"] = "NC"
    obs["observables"] = {"F2total": esf}
    obs["ProjectileDIS"] = "electron"
    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "bcd_d": "BCDMS_NC_EM_D_F2",
    "bcd_p": "BCDMS_NC_EM_P_F2",
}
# tmp0t2m7mk5
