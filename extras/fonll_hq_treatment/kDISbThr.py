"""Vary `kbThr` inside yadism."""
import copy
from typing import Tuple

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from utils import build_q2_obs, observables_card, theory_card

import yadism


def compute(kDISbThrs: list, curobs: list) -> Tuple[npt.ArrayLike, list]:
    """Compute data for given observables"""
    q2s = np.array([esf["Q2"] for esf in curobs])
    # prepare data
    oo = copy.deepcopy(observables_card)
    oo["observables"]["XSHERANC"] = curobs
    yads = []
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    # run yadism
    for kDISbThr in kDISbThrs:
        tt = copy.deepcopy(theory_card)
        # due to https://github.com/NNPDF/yadism/issues/167 we have to hack kqThr
        tt["kbThr"] = kDISbThr
        out = yadism.run_yadism(tt, oo)
        yad_data = out.apply_pdf_alphas_alphaqed_xir_xif(
            p, p.alphasQ, lambda _muR: tt["alphaqed"], 1.0, 1.0
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


# doit
kkDISbThrs = [1, 1.41, 2.0]
for xx, qq2s in [
    (1e-3, np.geomspace(18.0, 180.0, 30)),
    (1e-2, np.geomspace(18.0, 180.0, 30)),
    (1e-1, np.geomspace(18.0, 180.0, 30)),
]:
    plot_q2(xx, *compute(kkDISbThrs, build_q2_obs(xx, qq2s)), kkDISbThrs)
