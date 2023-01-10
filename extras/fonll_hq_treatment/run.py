import copy
from typing import Tuple

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from eko import interpolation

import yadism
import yadism.log
from yadmark.benchmark.external import apfel_utils

t = {
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

o = {
    "PolarizationDIS": 0.0,
    "ProjectileDIS": "positron",
    "PropagatorCorrection": 0.0,
    "TargetDIS": "proton",
    "interpolation_is_log": True,
    "interpolation_polynomial_degree": 4,
    "interpolation_xgrid": interpolation.make_lambert_grid(60),
    "observables": {"XSHERANC": []},
    "prDIS": "NC",
    "NCPositivityCharge": None,
}


def compute(curobs: list) -> Tuple[npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]:
    """Compute data for given observables"""
    # run yadism
    oo = copy.deepcopy(o)
    oo["observables"]["XSHERANC"] = curobs
    out = yadism.run_yadism(t, oo)

    # prepare data
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    yad_data = out.apply_pdf(p)
    apf_data = apfel_utils.compute_apfel_data(t, oo, p)
    xs = np.array([esf["x"] for esf in yad_data["XSHERANC"]])
    yads = np.array([esf["result"] for esf in yad_data["XSHERANC"]])
    apfs = np.array([esf["result"] for esf in apf_data["XSHERANC"]])
    return xs, yads, apfs


def plot_x(q2: float, xs: npt.ArrayLike, yads: npt.ArrayLike, apfs: npt.ArrayLike):
    """Plot with fixed Q2 and varying x"""
    fig = plt.figure()
    fig.suptitle(f"theory 400, NNPDF4.0, Q² = {q2} GeV²")
    ax0 = fig.add_subplot(3, 1, (1, 2))
    ax0.plot(xs, yads, label="yadism")
    ax0.plot(xs, apfs, label="APFEL")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.plot(xs, apfs / yads, label="APFEL/yadism")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Bjorken x")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"q2_{q2}.pdf")
    plt.close(fig)


def build_x_obs(q2: float, xs: npt.ArrayLike, s: float = 318.0**2) -> list:
    """Generate ESF with fixed Q2 and varying x"""
    obs = []
    for x in xs:
        obs.append(dict(Q2=q2, x=float(x), y=q2 / s / float(x)))
    return obs


# doit
for qq2, xxs in [
    (10.0, np.geomspace(1e-4, 5e-2, 20)),
    (18.0, np.geomspace(1e-4, 5e-2, 20)),
    (27.0, np.geomspace(1e-4, 5e-2, 20)),
    (45.0, np.geomspace(1e-4, 5e-2, 20)),
    (120.0, np.geomspace(1e-3, 2e-1, 20)),
    (400.0, np.geomspace(5e-3, 5e-1, 20)),
]:
    plot_x(qq2, *compute(build_x_obs(qq2, xxs)))
