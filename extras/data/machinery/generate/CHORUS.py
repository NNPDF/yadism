import pathlib

from .utils import load, obs_template, check_duplicate_kins

Mn = 0.9389


def dump(src_path, _target):
    """Compute CHORUS observables.

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

    if src.stem.split("_")[-1] == "pb":
        data = load(str(src), 0, ["-", "x", "Q2", "y"])
        esf = [dict(x=d["x"], y=d["y"], Q2=d["Q2"]) for d in data]
        obs["TargetDIS"] = "proton"
    else:
        data = load(src_path, 0, ["Enu", "x", "y"])
        esf = [
            dict(x=d["x"], y=d["y"], Q2=2.0 * Mn * d["x"] * d["y"] * d["Enu"])
            for d in data
        ]
        obs["TargetDIS"] = "lead"
    check_duplicate_kins(esf, subset=["x", "Q2", "y"])

    is_nu = "nu" in src_path.stem
    obs["prDIS"] = "CC"
    xs = "XSCHORUSCC"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "neutrino" if is_nu else "antineutrino"

    return obs


# renaming
new_names = {
    "x-sec_shift_nb": "CHORUS_CC_NB_PB_SIGMARED",
    "x-sec_shift_nu": "CHORUS_CC_NU_PB_SIGMARED",
    "chorus_nb_pb": "CHORUS_CC_NB_PB_SIGRED",
    "chorus_nu_pb": "CHORUS_CC_NU_PB_SIGRED",
}
