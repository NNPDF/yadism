# -*- coding: utf-8 -*-
import logging
import os
import pathlib

import matplotlib.colors as clr
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from . import parse

_logger = logging.getLogger(__name__)


def to_xarray(blocks: list[parse.Block]) -> xr.Dataset:
    catdict = {
        k: (["bl"], [getattr(dic, k) for dic in blocks]) for k in blocks[0].__dict__
    }
    catdict["grid"][0].extend(["x", "y"])
    catdict["xgrid"][0].append("z")

    return xr.Dataset(catdict)


def plot(ds: xr.Dataset, path: os.PathLike):
    path = pathlib.Path(path)

    plt.figure()
    ds["xgrid"].plot(norm=clr.LogNorm())
    figpath = path.with_stem(f"{path.stem}-xgrid")
    plt.savefig(figpath)

    _logger.info(f"Saved xgrid plot to {figpath.relative_to(pathlib.Path.cwd())}")

    plt.figure()
    xbj = ds["xbj"]
    nxbj = np.abs(np.log(xbj))
    (nxbj / nxbj.max()).plot(label="xBj")
    qc = ds["qcd_scale"]
    (qc / qc.max()).plot(label="qcd")
    en = ds["energy"]
    nen = np.log(en)
    (nen / nen.max()).plot(label="E")
    plt.ylabel("logs and ratios")
    plt.legend()
    plt.title(
        f"xBj = {xbj.min():0.3g} - {xbj.max():0.3g}\n"
        f"qcd = {qc.min()} - {qc.max()}\n"
        f"E = {en.min():0.3g} - {en.max():0.3g}"
    )
    plt.tight_layout()
    figpath = path.with_stem(f"{path.stem}-xbj-scales")
    plt.savefig(figpath)

    _logger.info(f"Saved xgrid plot to {figpath.relative_to(pathlib.Path.cwd())}")
