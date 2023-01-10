import copy
from typing import Tuple

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from eko import interpolation

import yadism

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


def compute(kDISbThrs: list, curobs: list) -> Tuple[npt.ArrayLike, list]:
    """Compute data for given observables"""
    q2s = np.array([esf["Q2"] for esf in curobs])
    # prepare data
    oo = copy.deepcopy(o)
    oo["observables"]["XSHERANC"] = curobs
    yads = []
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    # run yadism
    for kDISbThr in kDISbThrs:
        tt = copy.deepcopy(t)
        # due to https://github.com/NNPDF/yadism/issues/167 we have to hack kqThr
        tt["kbThr"] = kDISbThr
        out = yadism.run_yadism(tt, oo)
        yad_data = out.apply_pdf_alphas_alphaqed_xir_xif(
            p, p.alphasQ, lambda _muR: t["alphaqed"], 1.0, 1.0
        )
        # yad_data = out.apply_pdf(p)
        yads.append(np.array([esf["result"] for esf in yad_data["XSHERANC"]]))
    return q2s, yads


def plot_q2(x: float, q2s: npt.ArrayLike, yads: list, kDISbThrs: list):
    """Plot with fixed x and varying Q2"""
    fig = plt.figure()
    fig.suptitle(f"theory 400, NNPDF4.0, x = {x}")
    ax0 = fig.add_subplot(3, 1, (1, 2))
    for kDISbThr, yad in zip(kDISbThrs, yads):
        ax0.plot(q2s, yad, label=f"{kDISbThr}")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.plot([], [])  # do an empty plot to align the colors
    for kDISbThr, yad in zip(kDISbThrs[1:], yads[1:]):
        ax1.plot(q2s, yad / yads[0], label=f"{kDISbThr}")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Virtuality Q² [GeV²]")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"kDISbThr-x_{x}.pdf")
    plt.close(fig)


def build_q2_obs(x: float, q2s: npt.ArrayLike, s: float = 318.0**2) -> list:
    """Generate ESF with fixed x and varying Q2"""
    obs = []
    for q2 in q2s:
        obs.append(dict(Q2=q2, x=x, y=float(q2) / s / x))
    return obs


# doit
kkDISbThrs = [1, 1.41, 2.0]
for xx, qq2s in [
    (1e-3, np.geomspace(18.0, 180.0, 30)),
    (1e-2, np.geomspace(18.0, 180.0, 30)),
    (1e-1, np.geomspace(18.0, 180.0, 30)),
]:
    plot_q2(xx, *compute(kkDISbThrs, build_q2_obs(xx, qq2s)), kkDISbThrs)
