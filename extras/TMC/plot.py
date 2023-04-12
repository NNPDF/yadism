# -*- coding: utf-8 -*-
import pathlib
import sys

import lhapdf
import numpy as np
import yaml

from yadism import Runner

here = pathlib.Path(__file__).absolute().parent
sys.path.append(str(here.parents[1] / "benchmarks" / "aux"))
import toyLH  # pylint:disable=import-error,wrong-import-position

with open("theory.yaml") as theory_file:
    theory_template = yaml.full_load(theory_file)

with open("observables.yaml") as obs_file:
    obs = yaml.full_load(obs_file)

pdf_name = "ToyLH"
# setup PDFset
if pdf_name == "ToyLH":
    pdf = toyLH.mkPDF("ToyLH", 0)
else:
    pdf = lhapdf.mkPDF(pdf_name, 0)

# collect data
results = []
for TMC in range(4):
    theory_template["TMC"] = TMC
    r = Runner(theory_template, obs)
    results.append(r.apply(pdf)["F2light"])
# reorder data
arr = np.array(results)
print(arr.T)
