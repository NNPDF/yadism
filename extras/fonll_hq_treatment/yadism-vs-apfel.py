"""Compare yadsim against APFEL."""
import copy
from typing import Tuple

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from utils import build_q2_obs, build_x_obs, observables_card, theory_card

import yadism
import yadism.log
from yadmark.benchmark.external import apfel_utils


def compute(
    curobs: list,
) -> Tuple[npt.ArrayLike, npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]:
    """Compute data for given observables"""
    # run yadism
    oo = copy.deepcopy(observables_card)
    oo["observables"]["XSHERANC"] = curobs
    out = yadism.run_yadism(theory_card, oo)
    xs = np.array([esf["x"] for esf in curobs])
    q2s = np.array([esf["Q2"] for esf in curobs])

    # prepare data
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    yad_data = out.apply_pdf(p)
    apf_data = apfel_utils.compute_apfel_data(theory_card, oo, p)
    yads = np.array([esf["result"] for esf in yad_data["XSHERANC"]])
    apfs = np.array([esf["result"] for esf in apf_data["XSHERANC"]])
    return xs, q2s, yads, apfs


def plot_x(
    xs: npt.ArrayLike, q2s: npt.ArrayLike, yads: npt.ArrayLike, apfs: npt.ArrayLike
):
    """Plot with fixed Q2 and varying x"""
    q2 = q2s[0]
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
    fig.savefig(f"yadism-vs-apfel-q2_{q2}.pdf")
    plt.close(fig)


def plot_q2(
    xs: npt.ArrayLike, q2s: npt.ArrayLike, yads: npt.ArrayLike, apfs: npt.ArrayLike
):
    """Plot with fixed x and varying q2"""
    x = xs[0]
    fig = plt.figure()
    fig.suptitle(f"theory 400, NNPDF4.0, x = {x}")
    ax0 = fig.add_subplot(3, 1, (1, 2))
    ax0.plot(q2s, yads, label="yadism")
    ax0.plot(q2s, apfs, label="APFEL")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.plot(q2s, apfs / yads, label="APFEL/yadism")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Virtuality Q² [GeV²]")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"yadism-vs-apfel-x_{x}.pdf")
    plt.close(fig)


# doit
# for qq2, xxs in [
#     (10.0, np.geomspace(1e-4, 5e-2, 20)),
#     (18.0, np.geomspace(1e-4, 5e-2, 20)),
#     (27.0, np.geomspace(1e-4, 5e-2, 20)),
#     (45.0, np.geomspace(1e-4, 5e-2, 20)),
#     (120.0, np.geomspace(1e-3, 2e-1, 20)),
#     (400.0, np.geomspace(5e-3, 5e-1, 20)),
# ]:
#     plot_x(*compute(build_x_obs(qq2, xxs)))

for xx, qq2s in [
    # (2e-4, np.geomspace(15, 35, 30)),
    # (2e-3, np.geomspace(15, 35, 30)),
    (1e-3, np.geomspace(15, 35, 30)),
]:
    plot_q2(*compute(build_q2_obs(xx, qq2s)))
