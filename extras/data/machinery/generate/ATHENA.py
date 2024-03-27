import numpy as np

from .utils import *


def dump(src_path, target):
    """Generate the input card for ATHENA measurements.

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
    dict_kins = [dict(x=float(d[0]), y=float(d[2]), Q2=float(d[1])) for d in data]

    obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
    observable_name = "F1_total" if "_F1" in target.parent.name else "g1_total"
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
    "athena_29gev_ep": ["ATHENA_NC_29GEV_EP_G1", "ATHENA_NC_29GEV_EP_F1"],
    "athena_45gev_ep": ["ATHENA_NC_45GEV_EP_G1", "ATHENA_NC_45GEV_EP_F1"],
    "athena_63gev_ep": ["ATHENA_NC_63GEV_EP_G1", "ATHENA_NC_63GEV_EP_F1"],
    "athena_105gev_ep": ["ATHENA_NC_105GEV_EP_G1", "ATHENA_NC_105GEV_EP_F1"],
    "athena_140gev_ep": ["ATHENA_NC_140GEV_EP_G1", "ATHENA_NC_140GEV_EP_F1"],
}
