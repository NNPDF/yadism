# -*- coding: utf-8 -*-
import yaml

from .utils import obs_template


def dump(src_path, _target):
    """Compute positivity observables.

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
    with open(src_path, "r", encoding="utf-8") as f:
        obs_update = yaml.safe_load(f)
    obs.update(obs_update)
    obs["prDIS"] = "EM"
    obs["ProjectileDIS"] = "electron"
    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "u": "NNPDF_POS_F2U_40",
}
