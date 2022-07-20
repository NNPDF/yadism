# -*- coding: utf-8 -*-
import yaml

from .utils import obs_template


def _make_kins():
    """Generate kinematics.

    Routine is taken from https://github.com/NNPDF/nnpdf/blob/17952b40f02d23fc2b29a702ea93db6dc4e3b2fa/buildmaster/filters/POS.cc
    and meta data from https://github.com/NNPDF/nnpdf/blob/17952b40f02d23fc2b29a702ea93db6dc4e3b2fa/buildmaster/meta/POSF2U.yaml .
    """
    # from meta
    fNData = 20

    q2pos = 5  # GeV2
    xmin = 5e-7
    xmax = 0.9
    xch = 0.1
    nxposlog = fNData / 2
    step = (xmax - xch) / (fNData - nxposlog)

    xs = []
    for j in range(fNData):
        if j < nxposlog:
            xs.append(xmin * pow(xch / xmin, j / (nxposlog - 1)))
        else:
            xs.append(xch + step * (1 + j - nxposlog))
    return [{"Q2": q2pos, "x": x, "y": 1.0} for x in xs]


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
    obs["NCPositivityCharge"] = obs_update["NCPositivityCharge"]
    obs["observables"][obs_update["obs"]] = _make_kins()
    obs["prDIS"] = "EM"
    obs["ProjectileDIS"] = "electron"
    obs["TargetDIS"] = "proton"

    return obs


# renaming
new_names = {
    "u": "NNPDF_POS_F2U_40",
}
