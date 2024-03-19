from .utils import *
import numpy as np


def dump(src_path, target):
    """Generate the input card for EIC measurements.

    Parameters
    ----------
    src_path : str
        input path
    target: str
        target nucleon

    Returns
    -------
    dict
        observables dictionary, corresponding to the runcard

    """
    obs = obs_template.copy()
    data = np.genfromtxt(src_path)
    dict_kins = [dict(x=float(d[0]), y=0.0, Q2=float(d[1])) for d in data]

    obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
    observable_name = "F1_charm" if "_F1" in target.parent.name else "g1_charm"
    obs["observables"] = {observable_name: dict_kins}
    if "_ep_" in str(src_path.stem) or "_mup_" in str(src_path.stem):
        obs["TargetDIS"] = "proton"
    elif "_en_" in str(src_path.stem) or "_mun_" in str(src_path.stem):
        obs["TargetDIS"] = "neutron"
    elif "_ed_" in str(src_path.stem) or "_mud_" in str(src_path.stem):
        obs["TargetDIS"] = "isoscalar"

    # Details regarding the observables
    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"

    return obs


# renaming
new_names = {
    "EIcC_3_20_A1c_100fb-1": ["EIcC_NC_15GEV_EP_G1", "EIcC_NC_15GEV_EP_F1"],
    "EIcC_5_25_A1c_100fb-1": ["EIcC_NC_22GEV_EP_G1", "EIcC_NC_22GEV_EP_F1"],
}
