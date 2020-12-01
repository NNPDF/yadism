# -*- coding: utf-8 -*-
# pylint: skip-file
import pathlib
import numpy as np

import yaml
import lhapdf

import yadism

data = pathlib.Path(__file__).parent / "pineappl"

# read input
with open(data / "pineappl_sample_obs.yaml") as o:
    obs = yaml.safe_load(o)
with open(data / "pineappl_sample_theory.yaml") as o:
    theory = yaml.safe_load(o)

# run yadism
out = yadism.run_yadism(theory, obs)
out.dump_yaml_to_file(data / "pineappl_sample.yaml")

# apply uonly pdf
pdf_set = lhapdf.mkPDF("CT14llo_NF6",0)
pdf_out = out.apply_pdf(pdf_set)
pdf_out.dump_yaml_to_file(data / "pineappl_sample_CT14llo_NF6_0000.yaml")

# debug first element
# def list_pdfs(lhapdf_like, pids, Q2, xiF, xgrid):
#     # factorization scale
#     muF2 = Q2 * xiF ** 2
#     pdfs = np.zeros((len(pids), len(xgrid)))
#     for j, pid in enumerate(pids):
#         if not lhapdf_like.hasFlavor(pid):
#             continue
#         pdfs[j] = np.array([lhapdf_like.xfxQ2(pid, z, muF2) / z for z in xgrid])
#     return pdfs

# first_esf = out["F2total"][0]
# first_pdfs = list_pdfs(pdf_set,out["pids"],first_esf.Q2, out["xiF"], out["interpolation_xgrid"])
# u_idx = out["pids"].index(2)
# # store debug information
# debug_first = {
#     "x": out["interpolation_xgrid"].tolist(),
#     "grid": first_esf.values[u_idx].tolist(),
#     "xfx/x": first_pdfs[u_idx].tolist(),
# }
# with open(data / "debug_first.yaml", "w") as o:
#     yaml.safe_dump(debug_first, o)