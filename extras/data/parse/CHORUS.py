from .utils import load, obs_template

Mn = 0.9389


def dump(src_path):
    """
    Compute CHORUS observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    data = load(src_path, 2, ["Enu", "x", "y"])
    esf = [
        dict(x=d["x"], y=d["y"], Q2=2.0 * Mn * d["x"] * d["y"] * d["Enu"]) for d in data
    ]
    is_nu = "nu" in src_path.stem
    obs["prDIS"] = "CC"
    xs = "XSCHORUSCC"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "neutrino" if is_nu else "antineutrino"
    obs["TargetDIS"] = "lead"

    return obs


# renaming
new_names = {
    "x-sec_shift_nb": "CHORUS_CC_NB_PB_SIGMARED",
    "x-sec_shift_nu": "CHORUS_CC_NU_PB_SIGMARED",
}
