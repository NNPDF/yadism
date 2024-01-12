from .utils import check_duplicate_kins, load, obs_template

Mn = 0.9389


def dump(src_path, target):
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
    obs = obs_template.copy()

    data = load(src_path, 0, ["Enu", "x", "y"])
    esf = [
        dict(x=d["x"], y=d["y"], Q2=2.0 * Mn * d["x"] * d["y"] * d["Enu"]) for d in data
    ]
    tname = str(target).split("/")[-2]
    obs["TargetDIS"] = "proton" if "SIGRED" in tname else "lead"
    # TODO: addint the `y`-dimension should not be required here!
    check_duplicate_kins(esf, subset=["x", "Q2", "y"])

    is_nu = "nu" in src_path.stem
    obs["prDIS"] = "CC"
    xs = "XSCHORUSCC"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "neutrino" if is_nu else "antineutrino"

    return obs


# renaming
new_names = {
    "x-sec_shift_nb": ["CHORUS_CC_NB_PB_SIGMARED", "CHORUS_CC_NB_PB_SIGRED"],
    "x-sec_shift_nu": ["CHORUS_CC_NU_PB_SIGMARED", "CHORUS_CC_NU_PB_SIGRED"],
}
