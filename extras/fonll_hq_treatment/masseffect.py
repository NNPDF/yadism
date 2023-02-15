"""Vary `kbThr` inside yadism."""
import copy
import pathlib

import lhapdf
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pineappl
import yaml
from utils import (
    build_matrix_obs,
    build_q2_obs,
    compute_grids,
    dump_theory_cards,
    observables_card,
    update_theory,
    yaml_card,
)

obsfn_template = "masseffect-{obs_suffix}"


def dump_cards(curobs: list, obs_suffix: str):
    """Compute data for given observables"""
    # obs card
    oo = copy.deepcopy(observables_card)
    oo["observables"]["XSHERANC"] = curobs
    fn = obsfn_template.format(obs_suffix=obs_suffix)
    with open(f"./observable_cards/{fn}.yaml", "w", encoding="utf-8") as fd:
        yaml.safe_dump(oo, fd)
    # yaml card
    yy = copy.deepcopy(yaml_card)
    yy["operands"] = [[fn]]
    with open(f"./ymldb/{fn}.yaml", "w", encoding="utf-8") as fd:
        yaml.safe_dump(yy, fd)


def plot_q2_grid(upds: dict, obs_suffix: str):
    """Plot grids with fixed x and varying Q2"""
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    fig = plt.figure()
    ax0 = fig.add_subplot(3, 1, (1, 2))
    data = []
    for tid, upd in upds.items():
        tt = update_theory(upd)
        gp = pathlib.Path(f"./grids/{tid}/{obsfn}.pineappl.lz4")
        g = pineappl.grid.Grid.read(gp)
        conv = g.convolute_with_one(2212, p.xfxQ2, p.alphasQ2)
        data.append(conv)
        q2s = g.bin_left(0)
        xs = g.bin_left(1)
        ax0.plot(q2s, conv, label=f"{tt['FNS']}")
    x = xs[0]
    fig.suptitle(f"${{m_b,m_t}} \\geq 10^6$, NNPDF4.0, x = {x}")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.hlines(1.0, np.min(q2s), np.max(q2s), colors="#bbbbbb", linestyles="dashed")
    ax1.plot([], [])  # do an empty plot to align the colors
    for upd, conv in zip(list(upds.values())[1:], data[1:]):
        tt = update_theory(upd)
        ax1.plot(q2s, conv / data[0], label=f"{tt['FNS']}")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Virtuality Q² [GeV²]")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"masseffect-grid-x_{x}.pdf")
    plt.close(fig)


def plot_matrix(upds: dict, obs_suffix: str):
    """Plot grids with fixed x and varying Q2"""
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    fig = plt.figure(figsize=(13, 5))
    ax0 = fig.add_subplot(1, 2, 1)
    data = {}
    for tid in upds.keys():
        # tt = update_theory(upd)
        gp = pathlib.Path(f"./grids/{tid}/{obsfn}.pineappl.lz4")
        g = pineappl.grid.Grid.read(gp)
        conv = g.convolute_with_one(2212, p.xfxQ2, p.alphasQ2)
        q2s = np.log10(np.unique(g.bin_left(0)))
        xs = np.log10(np.unique(g.bin_left(1)))
        data[tid] = conv.reshape(len(xs), len(q2s)).T
    X, Y = np.meshgrid(xs, q2s)
    fig.suptitle("${{m_b,m_t}} \\geq 10^6$, NNPDF4.0")
    im = ax0.pcolormesh(X, Y, data[10], shading="auto")
    fig.colorbar(im, ax=ax0)
    ax0.set_title(r"$\sigma^{red}$ w/ FONLL")
    ax0.set_ylabel(r"$\log_{10}(Q^2)$")
    ax0.set_xlabel(r"$\log_{10}(x)$")
    ax1 = fig.add_subplot(1, 2, 2)
    im = ax1.pcolormesh(
        X,
        Y,
        data[10] / data[11],
        shading="auto",
        cmap=plt.colormaps["bwr"],
        norm=colors.CenteredNorm(1.0),
    )
    ax1.set_title("FONLL/ZM-VFNS")
    ax1.set_ylabel(r"$\log_{10}(Q^2)$")
    ax1.set_xlabel(r"$\log_{10}(x)$")
    fig.colorbar(im, ax=ax1)
    fig.tight_layout()
    fig.savefig("masseffect-matrix-grid.pdf")
    plt.close(fig)


# doit
fns_upds = {10: {"mb": 1e6, "mt": 1e8}, 11: {"mb": 1e6, "mt": 1e8, "FNS": "ZM-VFNS"}}
# dump_theory_cards(fns_upds)
# for xx, qq2s, suffix in [
#     (1e-3, np.geomspace(18.0, 540.0, 30), "1e-3"),
#     (1e-2, np.geomspace(18.0, 540.0, 30), "1e-2"),
#     (1e-1, np.geomspace(18.0, 540.0, 30), "1e-1"),
# ]:
#     # dump_cards(build_q2_obs(xx, qq2s), suffix)
#     # compute_grids(fns_upds.keys(), obsfn_template.format(obs_suffix=suffix))
#     plot_q2_grid(fns_upds, suffix)

xxs = np.geomspace(1e-4, 0.9, 20)
qq2s = np.geomspace(5, 500, 30)
suffix = "matrix"
# dump_cards(build_matrix_obs(xxs, qq2s),suffix)
# compute_grids(fns_upds.keys(), obsfn_template.format(obs_suffix=suffix))
plot_matrix(fns_upds, suffix)
