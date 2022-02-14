# -*- coding: utf-8 -*-
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
    obs = obs_template.copy()
    data = load(src_path, 0, ["-", "Enu", "y", "x"])
    esf = [
        dict(x=d["x"], y=d["y"], Q2=2.0 * mn * d["x"] * d["y"] * d["Enu"]) for d in data
    ]
    is_nu = "NU" in src_path.stem
    obs["prDIS"] = "CC"
    xs = "XSNUTEVCC_charm"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "neutrino" if is_nu else "antineutrino"
    obs["TargetDIS"] = "iron"

    return obs


# renaming
new_names = {
    "NTVNBDMNFe": "NUTEV_CC_NB_FE_SIGMARED",
    "NTVNUDMNFe": "NUTEV_CC_NU_FE_SIGMARED",
}
