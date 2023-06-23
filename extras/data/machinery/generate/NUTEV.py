import pathlib

from .utils import load, obs_template

mn = 0.938


def dump(src_path, _target):
    """Compute NUTEV observables.

    Parameters
    ----------
    src_path : str
        input path

    Returns
    -------
    dict
        observables dictionary, corresponding to the runcard

    """
    src = pathlib.Path(src_path)
    obs = obs_template.copy()

    if src.stem.split("_")[-1] == "Fe":
        data = load(str(src), 0, ["-", "x", "Q2", "y"])
        esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
        obs["TargetDIS"] = "proton"
    else:
        data = load(src_path, 0, ["-", "Enu", "y", "x"])
        esf = [
            dict(x=d["x"], y=d["y"], Q2=2.0 * mn * d["x"] * d["y"] * d["Enu"])
            for d in data
        ]
        obs["TargetDIS"] = "iron"

    is_nu = "NU" in src_path.stem
    obs["prDIS"] = "CC"
    xs = "XSNUTEVCC_charm"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "neutrino" if is_nu else "antineutrino"

    return obs


# renaming
new_names = {
    "NTVNBDMNFe": "NUTEV_CC_NB_FE_SIGMARED",
    "NTVNUDMNFe": "NUTEV_CC_NU_FE_SIGMARED",
    "NUTEV_NB_Fe": "NUTEV_NB_Fe",
    "NUTEV_NU_Fe": "NUTEV_NU_Fe",
}
