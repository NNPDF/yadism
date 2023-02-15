"""Investigation for heavy quark treatment."""

import copy
import pathlib

import numpy.typing as npt
import yaml
from eko import interpolation

import yadism
from yadbox.export import dump_pineappl_to_file

theory_card = {
    "ID": 400,
    "PTO": 2,
    "FNS": "FONLL-C",
    "DAMP": 0,
    "IC": 1,
    "IB": 0,
    "ModEv": "TRN",
    "ModSV": "unvaried",
    "XIR": 1.0,
    "XIF": 1.0,
    "fact_to_ren_scale_ratio": 1.0,
    "NfFF": 5,
    "MaxNfAs": 5,
    "MaxNfPdf": 5,
    "Q0": 1.65,
    "alphas": 0.118,
    "Qref": 91.2,
    "nf0": None,
    "nfref": None,
    "QED": 0,
    "alphaqed": 0.007496252,
    "Qedref": 1.777,
    "SxRes": 0,
    "SxOrd": "LL",
    "HQ": "POLE",
    "mc": 1.51,
    "Qmc": 1.51,
    "kcThr": 1.0,
    "mb": 4.92,
    "Qmb": 4.92,
    "kbThr": 1.0,
    "mt": 172.5,
    "Qmt": 172.5,
    "ktThr": 1.0,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    "MZ": 91.1876,
    "MW": 80.398,
    "GF": 1.1663787e-05,
    "SIN2TW": 0.23126,
    "TMC": 0,
    "MP": 0.938,
    "Comments": "NNPDF4.0 NNLO alphas=0.118",
    "global_nx": 0,
    "EScaleVar": 1,
    "kDIScThr": 1.0,
    "kDISbThr": 1.0,
    "kDIStThr": 1.0,
}

observables_card = {
    "PolarizationDIS": 0.0,
    "ProjectileDIS": "positron",
    "PropagatorCorrection": 0.0,
    "TargetDIS": "proton",
    "interpolation_is_log": True,
    "interpolation_polynomial_degree": 4,
    "interpolation_xgrid": interpolation.lambertgrid(
        60
    ).tolist(),  # interpolation.make_lambert_grid(60).tolist(),
    "observables": {"XSHERANC": []},
    "prDIS": "NC",
    "NCPositivityCharge": None,
}


yaml_card = {
    "conversion_factor": 1.0,
    "operands": [],
    "operation": None,
    "target_dataset": "",
}


def build_x_obs(q2: float, xs: npt.ArrayLike, s: float = 318.0**2) -> list:
    """Generate ESF with fixed Q2 and varying x."""
    obs = []
    for x in xs:
        obs.append(dict(Q2=q2, x=float(x), y=q2 / s / float(x)))
    return obs


def build_q2_obs(x: float, q2s: npt.ArrayLike, s: float = 318.0**2) -> list:
    """Generate ESF with fixed x and varying Q2."""
    obs = []
    for q2 in q2s:
        obs.append(dict(Q2=float(q2), x=x, y=float(q2) / s / x))
    return obs


def build_matrix_obs(xs: float, q2s: npt.ArrayLike, s: float = 318.0**2) -> list:
    """Generate ESF."""
    obs = []
    for x in xs:
        for q2 in q2s:
            obs.append(dict(Q2=float(q2), x=float(x), y=float(q2) / s / float(x)))
    return obs


def update_theory(upd: dict) -> dict:
    """Create a new theory card from an update."""
    tt = copy.deepcopy(theory_card)
    tt.update(upd)
    return tt


def dump_theory_cards(upds: dict):
    """Dump theory cards."""
    # theory cards
    for tid, upd in upds.items():
        tt = update_theory(upd)
        with open(f"./theory_cards/{tid}.yaml", "w", encoding="utf-8") as fd:
            yaml.safe_dump(tt, fd)


def compute_grids(tids: list, obsfn: str):
    """Compute data for given observables"""
    with open(f"./observable_cards/{obsfn}.yaml", encoding="utf-8") as fd:
        oo = yaml.safe_load(fd)
    # run yadism
    for tid in tids:
        with open(f"./theory_cards/{tid}.yaml", encoding="utf-8") as fd:
            tt = yaml.safe_load(fd)
        out = yadism.run_yadism(tt, oo)
        gp = pathlib.Path(f"./grids/{tid}/{obsfn}.pineappl.lz4")
        gp.parent.mkdir(exist_ok=True)
        dump_pineappl_to_file(out, gp, "XSHERANC")
