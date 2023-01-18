import pathlib

import eko
import lhapdf
import matplotlib.pyplot as plt
import numpy as np
from ekomark.apply import apply_pdf

obsfn_template = "kDISbThr-{obs_suffix}"


def plot_q2(kDISbThrs: dict, pid: int, xidx: int, obs_suffix: str):
    obsfn = obsfn_template.format(obs_suffix=obs_suffix)
    p = lhapdf.mkPDF("NNPDF40_nnlo_as_01180", 0)
    data = {}
    for tid, _kDISbThr in kDISbThrs.items():
        ep = pathlib.Path(f"./ekos/{tid}/{obsfn}.tar")
        op = eko.output.Output.load_tar(ep)
        evolved_pdfs = apply_pdf(op, p)
        x = op["interpolation_xgrid"][xidx]
        dat = []
        for q2, pdfs in evolved_pdfs.items():
            dat.append([q2, pdfs["pdfs"][pid][xidx]])
        data[tid] = np.array(dat)
    q2s = data[0][:, 0]
    fig = plt.figure()
    fig.suptitle(f"theory 400, NNPDF4.0, pid={pid}, x = {x}")
    ax = fig.add_subplot(111)
    ax.hlines(1.0, np.min(q2s), np.max(q2s), colors="#bbbbbb", linestyles="dashed")
    for tid, kDISbThr in kDISbThrs.items():
        if tid == 0:
            continue
        ax.plot(q2s, data[tid][:, 1] / data[0][:, 1], label=kDISbThr)
    ax.set_ylabel("ratio to µ=1")
    ax.set_xlabel("Q² [GeV²]")
    ax.set_xscale("log")
    ax.legend()
    fig.savefig(f"check-eko-pid_{pid}-xidx_{xidx}-suffix_{obs_suffix}.pdf")
    plt.close(fig)


kkDISbThrs = {0: 1, 1: 1.41, 2: 2.0}
for ppid in [21, 1, -1, 2, -2]:
    for xxidx in [10, 20, 30]:
        plot_q2(kkDISbThrs, ppid, xxidx, "1e-3")
