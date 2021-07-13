import argparse
import pathlib

import numpy as np
import yaml

here = pathlib.Path(__file__).parent

pineapple_xgrid = [
    1.9999999999999954e-07,
    3.034304765867952e-07,
    4.6035014748963906e-07,
    6.984208530700364e-07,
    1.0596094959101024e-06,
    1.607585498470808e-06,
    2.438943292891682e-06,
    3.7002272069854957e-06,
    5.613757716930151e-06,
    8.516806677573355e-06,
    1.292101569074731e-05,
    1.9602505002391748e-05,
    2.97384953722449e-05,
    4.511438394964044e-05,
    6.843744918967896e-05,
    0.00010381172986576898,
    0.00015745605600841445,
    0.00023878782918561914,
    0.00036205449638139736,
    0.0005487795323670796,
    0.0008314068836488144,
    0.0012586797144272762,
    0.0019034634022867384,
    0.0028738675812817515,
    0.004328500638820811,
    0.006496206194633799,
    0.009699159574043398,
    0.014375068581090129,
    0.02108918668378717,
    0.030521584007828916,
    0.04341491741702269,
    0.060480028754447364,
    0.08228122126204893,
    0.10914375746330703,
    0.14112080644440345,
    0.17802566042569432,
    0.2195041265003886,
    0.2651137041582823,
    0.31438740076927585,
    0.3668753186482242,
    0.4221667753589648,
    0.4798989029610255,
    0.5397572337880445,
    0.601472197967335,
    0.6648139482473823,
    0.7295868442414312,
    0.7956242522922756,
    0.8627839323906108,
    0.9309440808717544,
    1,
]


def load(path, skip):
    """
    Load esf kinematics from file

    Parameters
    ----------
        path : str
            file path

    Returns
    -------
        list(dict)
            list of ESF
    """
    data = np.loadtxt(path, skiprows=skip)
    data = data[:, :3]
    return [dict(zip(["Q2", "x", "y"], d.tolist())) for d in data]


# Load obs template
with open(here / "observable_template.yaml") as o:
    obs_template = yaml.safe_load(o)
obs_template["interpolation_xgrid"] = pineapple_xgrid


def dump_HERACOMB(src_path, target_path):
    """
    Write HERACOMB observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    esf = load(src_path, 2)
    is_cc = "CC" in src_path.stem
    obs["prDIS"] = "CC" if is_cc else "NC"
    xs = "XSHERACC" if is_cc else "XSHERANC"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "electron" if "EM" in src_path.stem else "positron"
    with open(target_path, "w") as o:
        yaml.safe_dump(obs, o)


def dump_HERACOMB_heavy(src_path, target_path):
    """
    Write HERACOMB heavy observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    esf = load(src_path, 36)
    obs["prDIS"] = "NC"
    xs = "XSHERANCAVG"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "electron"
    with open(target_path, "w") as o:
        yaml.safe_dump(obs, o)


# renaming
new_names = {
    "HERACOMBCCEM": "HERA_CC_318GEV_EM_SIGMARED",
    "HERACOMBCCEP": "HERA_CC_318GEV_EP_SIGMARED",
    "HERACOMBNCEM": "HERA_NC_318GEV_EM_SIGMARED",
    "HERACOMBNCEP460": "HERA_NC_225GEV_EP_SIGMARED",
    "HERACOMBNCEP575": "HERA_NC_251GEV_EP_SIGMARED",
    "HERACOMBNCEP820": "HERA_NC_300GEV_EP_SIGMARED",
    "HERACOMBNCEP920": "HERA_NC_318GEV_EP_SIGMARED",
    "d18-037.tableCharm": "HERA_NC_318GEV_EAVG_SIGMARED_CHARM",
    "d18-037.tableBeauty": "HERA_NC_318GEV_EAVG_SIGMARED_BOTTOM",
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
        if path.parent.stem == "HERACOMB":
            dump_HERACOMB(path, target)
        elif path.parent.stem in ["HERACOMB_SIGMARED_C", "HERACOMB_SIGMARED_B"]:
            dump_HERACOMB_heavy(path, target)
