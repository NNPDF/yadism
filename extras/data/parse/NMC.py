import pathlib
import tempfile

from .utils import load, obs_template


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
        for sub in src.glob("*"):
            text = sub.read_text()
            with tempfile.NamedTemporaryFile(mode="w") as ntf:
                cut_text = "\n".join(text.splitlines()[::2])
                ntf.write(cut_text)
                ntf.flush()
                data = load(ntf.name, 0, ["x", "Q2", "y"])
                esf += [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
        obs["observables"] = {"XSHERANC": esf}
        obs["TargetDIS"] = "proton"
    else:
        data = load(str(src), 0, ["x", "Q2"])
        esf = [dict(x=d["x"], y=1.0, Q2=d["Q2"]) for d in data]
        obs["observables"] = {"F2_total": esf}
        obs["TargetDIS"] = "proton" if "_P_" in target.name else "isoscalar"

    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"

    return obs


# renaming
new_names = {
    "nmc_p": "NMC_NC_EM_P_SIGMARED",
    "nmc_f2df2p": ["NMC_NC_EM_P_F2", "NMC_NC_EM_D_F2"],
}
