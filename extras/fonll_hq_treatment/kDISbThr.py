"""Vary `kbThr` inside yadism."""
import copy
import pathlib

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import pineappl
import yaml
from utils import build_q2_obs, observables_card, theory_card, yaml_card

import yadism
from yadbox.export import dump_pineappl_to_file

obsfn_template = "kDISbThr-{obs_suffix}"


def dump_cards(kDISbThrs: dict, curobs: list, obs_suffix: str):
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
    # theory cards
    for tid, kDISbThr in kDISbThrs.items():
        tt = copy.deepcopy(theory_card)
        # due to https://github.com/NNPDF/yadism/issues/167 we have to hack kqThr
        tt["kbThr"] = float(kDISbThr)
        with open(f"./theory_cards/{tid}.yaml", "w", encoding="utf-8") as fd:
            yaml.safe_dump(tt, fd)


def compute_grids(kDISbThrs: dict, obs_suffix: str):
    """Compute data for given observables"""
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    with open(f"./observable_cards/{obsfn}.yaml", encoding="utf-8") as fd:
        oo = yaml.safe_load(fd)
    # run yadism
    for tid in kDISbThrs.keys():
        with open(f"./theory_cards/{tid}.yaml", encoding="utf-8") as fd:
            tt = yaml.safe_load(fd)
        out = yadism.run_yadism(tt, oo)
        gp = pathlib.Path(f"./grids/{tid}/{obsfn}.pineappl.lz4")
        gp.parent.mkdir(exist_ok=True)
        dump_pineappl_to_file(out, gp, "XSHERANC")


def plot_q2_grid(kDISbThrs: dict, obs_suffix: str):
    """Plot grids with fixed x and varying Q2"""
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    fig = plt.figure()
    ax0 = fig.add_subplot(3, 1, (1, 2))
    data = []
    for tid, kDISbThr in kDISbThrs.items():
        gp = pathlib.Path(f"./grids/{tid}/{obsfn}.pineappl.lz4")
        g = pineappl.grid.Grid.read(gp)
        conv = g.convolute_with_one(2212, p.xfxQ2, p.alphasQ2)
        data.append(conv)
        q2s = g.bin_left(0)
        xs = g.bin_left(1)
        ax0.plot(q2s, conv, label=f"{kDISbThr}")
    x = xs[0]
    fig.suptitle(f"theory 400, NNPDF4.0, x = {x}")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.hlines(1.0, np.min(q2s), np.max(q2s), colors="#bbbbbb", linestyles="dashed")
    ax1.plot([], [])  # do an empty plot to align the colors
    for kDISbThr, conv in zip(list(kDISbThrs.values())[1:], data[1:]):
        ax1.plot(q2s, conv / data[0], label=f"{kDISbThr}")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Virtuality Q² [GeV²]")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"kDISbThr-grid-x_{x}.pdf")
    plt.close(fig)


def plot_q2_fk(kDISbThrs: dict, obs_suffix: str):
    """Plot fk tables with fixed x and varying Q2"""
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    fig = plt.figure()
    ax0 = fig.add_subplot(3, 1, (1, 2))
    data = []
    for tid, kDISbThr in kDISbThrs.items():
        gp = pathlib.Path(f"./fktables/{tid}/{obsfn}.pineappl.lz4")
        g = pineappl.fk_table.FkTable.read(gp)
        conv = g.convolute_with_one(2212, p.xfxQ2)
        data.append(conv)
        q2s = g.bin_left(0)
        xs = g.bin_left(1)
        ax0.plot(q2s, conv, label=f"{kDISbThr}")
    x = xs[0]
    fig.suptitle(f"theory 400, NNPDF4.0, x = {x}")
    ax0.set_ylabel(r"$\sigma^{red}$")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend()
    ax1 = fig.add_subplot(3, 1, 3, sharex=ax0)
    ax1.hlines(1.0, np.min(q2s), np.max(q2s), colors="#bbbbbb", linestyles="dashed")
    ax1.plot([], [])  # do an empty plot to align the colors
    for kDISbThr, conv in zip(list(kDISbThrs.values())[1:], data[1:]):
        ax1.plot(q2s, conv / data[0], label=f"{kDISbThr}")
    ax1.set_ylabel("ratio")
    ax1.set_xlabel("Virtuality Q² [GeV²]")
    ax1.set_xscale("log")
    ax1.legend()
    fig.savefig(f"kDISbThr-fk-x_{x}.pdf")
    plt.close(fig)


# doit
kkDISbThrs = {0: 1, 1: 1.41, 2: 2.0}
for xx, qq2s, suffix in [
    (1e-3, np.geomspace(18.0, 180.0, 30), "1e-3"),
    (1e-2, np.geomspace(18.0, 180.0, 30), "1e-2"),
    (1e-1, np.geomspace(18.0, 180.0, 30), "1e-1"),
]:
    # dump_cards(kkDISbThrs, build_q2_obs(xx, qq2s), suffix)
    # compute_grids(kkDISbThrs, suffix)
    plot_q2_grid(kkDISbThrs, suffix)
    plot_q2_fk(kkDISbThrs, suffix)
