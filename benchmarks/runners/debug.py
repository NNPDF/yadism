# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
# Our testing playground
import copy

import numpy as np
import pandas as pd
import pdb
import pathlib

here = pathlib.Path(__file__).parent

import lhapdf
from yadism import ic
from yadism.partonic_channel import PartonicChannelHeavyIntrinsic
from yadmark.data import observables
from yadmark.benchmark.external import apfel_utils as  apfel_here
from banana.data import theories
from banana.benchmark.external import apfel_utils


mc = 1.51
mc2 = mc**2

tcard = theories.default_card.copy()
tcard["mc"] = mc
tcard["IC"] = 1
ocard = observables.default_card.copy()
apfel = apfel_here.load_apfel(tcard,ocard,"conly")
#apfel.F2charm(x)
#print(apfel_data)

with open(here / "out.txt") as of:
    odata = pd.read_csv(of, sep="\s+",header=None)
kins = odata[::2]
kins.drop([0,4,5,6],inplace=True,axis=1)
kins.columns = ["Q2", "m1sq", "m2sq"]
kins.reset_index(drop=True,inplace=True)
vars = odata[1::2]
vars.drop([0],inplace=True,axis=1)
vars.columns = "I1,Cplus,C1m,C1p,CRm,S".split(",")
vars.reset_index(drop=True,inplace=True)
odata = pd.concat([kins,vars],axis=1)


for e in odata.iloc:
    class MockESF:
        pass
    esf = MockESF
    esf.x = np.nan
    esf.Q2 = e["Q2"]

    pc = PartonicChannelHeavyIntrinsic(esf,e["m1sq"], e["m2sq"])
    pc.init_nlo_vars()

    Sref = float(e["S"])
    
    if abs(pc.S - Sref) > 1e-6 or abs(pc.S/Sref - 1) > 1e-6:
        print(pc.S,Sref)



pdb.set_trace()