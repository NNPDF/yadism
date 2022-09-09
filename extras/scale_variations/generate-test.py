# -*- coding: utf-8 -*-
import copy

from eko import interpolation

import yadism
import yadism.log

t = {
    "ID": 208,
    "PTO": 1,
    "FNS": "FFNS",
    "DAMP": 0,
    "IC": 1,
    "IB": 0,
    "ModEv": "TRN",
    "ModSV": "unvaried",
    "XIR": 1.0,
    "XIF": 2.0,
    "fact_to_ren_scale_ratio": 1.0,
    "NfFF": 5,
    "MaxNfAs": 5,
    "MaxNfPdf": 5,
    "Q0": 1.65,
    "alphas": 0.118,
    "Qref": 91.2,
    "nf0": None,
    "nfref": None,
    "QED": 0,
    "alphaqed": 0.007496252,
    "Qedref": 1.777,
    "SxRes": 0,
    "SxOrd": "LL",
    "HQ": "POLE",
    "mc": 1.51,
    "Qmc": 1.51,
    "kcThr": 0.0,
    "mb": 4.92,
    "Qmb": 4.92,
    "kbThr": 0.0,
    "mt": 172.5,
    "Qmt": 172.5,
    "ktThr": 1.0,
    "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
    "MZ": 91.1876,
    "MW": 80.398,
    "GF": 1.1663787e-05,
    "SIN2TW": 0.23126,
    "TMC": 0,
    "MP": 0.938,
    "Comments": "NNPDF4.0 NLO alphas=0.118",
    "global_nx": 0,
    "EScaleVar": 1,
    "kDIScThr": 0.0001,
    "kDISbThr": 0.0001,
    "kDIStThr": 1.0,
}

o = {
    "PolarizationDIS": 0.0,
    "ProjectileDIS": "electron",
    "PropagatorCorrection": 0.0,
    "TargetDIS": "proton",
    "interpolation_is_log": True,
    "interpolation_polynomial_degree": 4,
    "interpolation_xgrid": [],
    "observables": {"F2_light": []},
    "prDIS": "EM",
}

# setup grids
grids = [
    interpolation.make_lambert_grid(30),
    interpolation.make_lambert_grid(60),
    interpolation.make_lambert_grid(90),
    interpolation.make_lambert_grid(120),
    interpolation.make_lambert_grid(150),
]
# run yadism
yadism.log.setup(log_to_stdout=False)
for j, grid in enumerate(grids):
    oo = copy.deepcopy(o)
    oo["interpolation_xgrid"] = grid.tolist()
    obs = []
    for x in grid:
        obs.append(dict(Q2=300.0, x=x))
    oo["observables"]["F2_light"] = obs
    out = yadism.run_yadism(t, oo)
    out.dump_pineappl_to_file(f"test{j}.pineappl.lz4", "F2_light")
