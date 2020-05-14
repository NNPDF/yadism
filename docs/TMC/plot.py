# -*- coding: utf-8 -*-
import pathlib
import sys

import numpy as np

from yadism import Runner
import lhapdf

here = pathlib.Path(__file__).absolute().parents[2]
sys.path.append(str(here / "benchmarks" / "aux"))
import toyLH  # pylint:disable=import-error,wrong-import-position

theory_template = {'ID': 22,
 'PTO': 0,
 'FNS': 'FFNS',
 'DAMP': 0,
 'IC': 0,
 'ModEv': 'EXA',
 'XIR': 1.0,
 'XIF': 1.0,
 'NfFF': 3,
 'MaxNfAs': 3,
 'MaxNfPdf': 3,
 'Q0': 1.275,
 'alphas': 0.11800000000000001,
 'Qref': 91.2,
 'QED': 0,
 'alphaqed': 0.007496251999999999,
 'Qedref': 1.777,
 'SxRes': 0,
 'SxOrd': 'LL',
 'HQ': 'POLE',
 'mc': 1.275,
 'Qmc': 1.275,
 'kcThr': 1.0,
 'mb': 4.18,
 'Qmb': 4.18,
 'kbThr': 1.0,
 'mt': 173.07,
 'Qmt': 173.07,
 'ktThr': 1.0,
 'CKM': '0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152',
 'MZ': 91.1876,
 'MW': 80.398,
 'GF': 1.1663787e-05,
 'SIN2TW': 0.23126,
 'TMC': 0,
 'MP': 0.938,
 'Comments': 'LO baseline for small-x res',
 'global_nx': 0,
 'EScaleVar': 1,
 '_modify_time': '2020-05-08 17:55:04.853875'}

obs = {'xgrid': [
  0.15,
  0.22727272727272727,
  0.30454545454545456,
  0.38181818181818183,
  0.4590909090909091,
  0.5363636363636364,
  0.6136363636363636,
  0.6909090909090909,
  0.7681818181818182,
  0.8454545454545455,
  0.9227272727272727,
  1.0],
 'polynomial_degree': 4,
 'is_log_interpolation': True,
 'prDIS': 'EM',
 'comments': '',
 '_modify_time': '2020-05-14 15:04:12.889845',
 'F2light': [
  {'x': 0.5, 'Q2': 20.0},
  {'x': 0.7, 'Q2': 20.0},
  {'x': 0.9, 'Q2': 20.0},
  {'x': 0.9, 'Q2': 10.0},
  ]}

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
