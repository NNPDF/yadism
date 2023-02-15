"""Vary `kbThr` inside yadism."""
import copy
import pathlib

import lhapdf
import matplotlib.pyplot as plt
import numpy as np
import pineappl
import yaml
from utils import (
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


# doit
fns_upds = {10: {"mb": 1e6, "mt": 1e8}, 11: {"mb": 1e6, "mt": 1e8, "FNS": "ZM-VFNS"}}
for xx, qq2s, suffix in [
    (1e-3, np.geomspace(18.0, 540.0, 30), "1e-3"),
    (1e-2, np.geomspace(18.0, 540.0, 30), "1e-2"),
    (1e-1, np.geomspace(18.0, 540.0, 30), "1e-1"),
]:
    # dump_cards(build_q2_obs(xx, qq2s), suffix)
    # dump_theory_cards(fns_upds)
    # compute_grids(fns_upds.keys(), obsfn_template.format(obs_suffix=suffix))
    plot_q2_grid(fns_upds, suffix)
