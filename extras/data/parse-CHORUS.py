import argparse

import yaml
from utils import here, load, obs_template

Mn = 0.9389


def dump_CHORUS(src_path, target_path):
    """
    Write CHORUS observables.

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
    with open(target_path, "w") as o:
        yaml.safe_dump(obs, o)


# renaming
new_names = {
    "x-sec_shift_nb": "CHORUS_CC_NB_PB_SIGMARED",
    "x-sec_shift_nu": "CHORUS_CC_NU_PB_SIGMARED",
}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    args = ap.parse_args()
    for i in args.inputs:
        path = here / i
        new_name = new_names[path.stem]
        target = here / new_name / "observable.yaml"
        target.parent.mkdir(exist_ok=True)
        print(f"Writing {path} to {target}")
        dump_CHORUS(path, target)
