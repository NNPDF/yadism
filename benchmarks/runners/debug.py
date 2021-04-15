# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import pdb
import pathlib

here = pathlib.Path(__file__).parent

import lhapdf
from yadism import ic
from yadism.partonic_channel import PartonicChannelHeavyIntrinsic
from yadmark.data import observables
from yadmark.benchmark.external import apfel_utils as apfel_here
from banana.data import theories
from banana.benchmark.external import apfel_utils


mc = 1.51
mc2 = mc ** 2


def call_apfel():
    tcard = theories.default_card.copy()
    tcard["mc"] = mc
    tcard["IC"] = 1
    ocard = observables.default_card.copy()
    apfel = apfel_here.load_apfel(tcard, ocard, "conly")
    # apfel.F2charm(x)
    # print(apfel_data)


def analyze_soft():
    with open(here / "out.txt") as of:
        odata = pd.read_csv(of, sep="\s+", header=None)
    kins = odata[::2]
    kins.drop([0, 4, 5, 6], inplace=True, axis=1)
    kins.columns = ["Q2", "m1sq", "m2sq"]
    kins.reset_index(drop=True, inplace=True)
    vars = odata[1::2]
    vars.drop([0], inplace=True, axis=1)
    vars.columns = "I1,Cplus,C1m,C1p,CRm,S".split(",")
    vars.reset_index(drop=True, inplace=True)
    odata = pd.concat([kins, vars], axis=1)

    for e in odata.iloc:

        class MockESF:
            pass

        esf = MockESF
        esf.x = np.nan
        esf.Q2 = e["Q2"]

        pc = PartonicChannelHeavyIntrinsic(esf, e["m1sq"], e["m2sq"])
        pc.init_nlo_vars()

        Sref = float(e["S"])
        if abs(pc.S - Sref) > 1e-6 and abs(pc.S / Sref - 1) > 1e-6:
            print("S", e["Q2"], e["m1sq"], e["m2sq"], pc.S, Sref)

        CRmref = float(e["CRm"])
        if abs(pc.CRm - CRmref) > 1e-6 and abs(pc.CRm / CRmref - 1) > 1e-6:
            print("CRm", e["Q2"], e["m1sq"], e["m2sq"], pc.CRm, CRmref)


def analyze_fhat():
    with open(here / "fhat.txt") as of:
        odata = pd.read_csv(of, sep="\s+", header=None)
        odata.columns = ["tag", "z", "Q2", "m1sq", "m2sq", "apf", "Splus", "Sminus"]
    f1hat = odata[odata["tag"] == "f1hat"]
    f1hat.drop(["tag"], inplace=True, axis=1)
    f2hat = odata[odata["tag"] == "f2hat"]
    f2hat.drop(["tag"], inplace=True, axis=1)

    class MockESF:
        pass

    esf = MockESF

    def yadf1hat(efhat):
        esf.x = 0.1
        esf.Q2 = efhat["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, efhat["m1sq"], efhat["m2sq"])
        pc.init_vars(efhat["z"])
        pc.init_nlo_vars()
        return efhat["Splus"] * ic.f1_splus_raw(pc) + efhat[
            "Sminus"
        ] * ic.f1_sminus_raw(pc)

    def yadf2hat(efhat):
        esf.x = 0.1
        esf.Q2 = efhat["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, efhat["m1sq"], efhat["m2sq"])
        pc.init_vars(efhat["z"])
        pc.init_nlo_vars()
        return efhat["Splus"] * ic.f2_splus_raw(pc) + efhat[
            "Sminus"
        ] * ic.f2_sminus_raw(pc)

    f1hat["yad"] = f1hat.apply(yadf1hat, axis=1)
    f2hat["yad"] = f2hat.apply(yadf2hat, axis=1)
    f1hat.reset_index(drop=True, inplace=True)
    f2hat.reset_index(drop=True, inplace=True)

    def apf_ratio(n1, n2):
        assert f2hat["Q2"][n1] == f2hat["Q2"][n2]
        f2 = f2hat["apf"]
        f1 = f1hat["apf"]
        return (f2[n1] / f1[n1]) / (f2[n2] / f1[n2])

    def yad_ratio(n1, n2):
        assert f2hat["Q2"][n1] == f2hat["Q2"][n2]
        f2 = f2hat["yad"]
        f1 = f1hat["yad"]
        return (f2[n1] / f1[n1]) / (f2[n2] / f1[n2])
    def ratio(start, diff):
        n1 = start
        n2 = start + diff
        print(f"z1: {f2hat['z'][n1]:.3e} - z2: {f2hat['z'][n2]:.3e} --- Q2: {f2hat['Q2'][n1]:.3f}")
        print("apf:", apf_ratio(n1, n2))
        print("yad:", yad_ratio(n1, n2))
    start = 0
    diff = 0
    ratio(start, diff)
    for diff in [2,4,6]:
        print(f"\n\t--- diff {diff} scan ---")
        for start in range(4030,10000,717):
            ratio(start, diff)

    for start in [3000, 5120, 8150]:
        print(f"\n\t--- start {start} scan ---")
        for diff in range(1,10):
            ratio(start, diff)

    pdb.set_trace()


if __name__ == "__main__":
    #  call_apfel()
    # analyze_fhat()
    analyze_soft()
