# -*- coding: utf-8 -*-
# pylint: skip-file
import pdb
import pathlib
import argparse

import numpy as np
import pandas as pd

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
    with open(here / "SV.txt") as of:
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

        esf = MockESF()
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


def analyze_soft1():
    with open(here / "SV1.txt") as of:
        odata = pd.read_csv(of, sep="\s+", header=None)
    soft = odata[odata[0] == "Soft"].copy()
    soft.drop([0], inplace=True, axis=1)
    soft.columns = ["Q2", "m1sq", "m2sq", "apf"]
    soft.reset_index(drop=True, inplace=True)
    virt1 = odata[odata[0] == "Virtual1"].copy()
    virt1.drop([0], inplace=True, axis=1)
    virt1.columns = ["Q2", "m1sq", "m2sq", "apf"]
    virt1.reset_index(drop=True, inplace=True)
    virt2 = odata[odata[0] == "Virtual2"].copy()
    virt2.drop([0], inplace=True, axis=1)
    virt2.columns = ["Q2", "m1sq", "m2sq", "apf"]
    virt2.reset_index(drop=True, inplace=True)

    class MockESF:
        pass

    def mysoft(e):
        esf = MockESF()
        esf.x = np.nan
        esf.Q2 = e["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, e["m1sq"], e["m2sq"])
        pc.init_nlo_vars()
        return pc.S

    def myvirt1(e):
        esf = MockESF()
        esf.x = 1.0
        esf.Q2 = e["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, e["m1sq"], e["m2sq"])
        pc.init_nlo_vars()
        return (ic.f1_splus_virt(pc) + ic.f1_sminus_virt(pc)) / (
            ic.M1splus(pc) + ic.M1sminus(pc)
        )

    def myvirt2(e):
        esf = MockESF()
        esf.x = 1.0
        esf.Q2 = e["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, e["m1sq"], e["m2sq"])
        pc.init_nlo_vars()
        return (ic.f2_splus_virt(pc) + ic.f2_sminus_virt(pc)) / (
            ic.M2splus(pc) + ic.M2sminus(pc)
        )

    soft["yad"] = soft.apply(mysoft, axis=1)
    soft["ratio"] = soft["yad"] / soft["apf"]
    virt1["yad"] = virt1.apply(myvirt1, axis=1)
    virt1["ratio"] = virt1["yad"] / virt1["apf"]
    virt2["yad"] = virt2.apply(myvirt2, axis=1)
    virt2["ratio"] = virt2["yad"] / virt2["apf"]

    __import__("pdb").set_trace()


def analyze_fhat():
    with open(here / "fhat.txt") as of:
        odata = pd.read_csv(of, sep="\s+", header=None)
        odata.columns = ["tag", "z", "Q2", "m1sq", "m2sq", "apf", "Splus", "Sminus"]
    f1hat = odata[odata["tag"] == "f1hat"].copy()
    f1hat.drop(["tag"], inplace=True, axis=1)
    f2hat = odata[odata["tag"] == "f2hat"].copy()
    f2hat.drop(["tag"], inplace=True, axis=1)
    f1tilde = odata[odata["tag"] == "f1tilde"].copy()
    f1tilde.drop(["tag"], inplace=True, axis=1)
    f2tilde = odata[odata["tag"] == "f2tilde"].copy()
    f2tilde.drop(["tag"], inplace=True, axis=1)

    class MockESF:
        pass

    esf = MockESF()

    def yadf1tilde(efhat):
        esf.x = 0.1
        esf.Q2 = efhat["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, efhat["m1sq"], efhat["m2sq"])
        pc.init_vars(efhat["z"])
        pc.init_nlo_vars()
        return (ic.f1_splus_raw(pc) + ic.f1_sminus_raw(pc)) / (
            ic.M1splus(pc) + ic.M1sminus(pc)
        )

    def yadf2tilde(efhat):
        esf.x = 0.1
        esf.Q2 = efhat["Q2"]
        pc = PartonicChannelHeavyIntrinsic(esf, efhat["m1sq"], efhat["m2sq"])
        pc.init_vars(efhat["z"])
        pc.init_nlo_vars()
        return (ic.f2_splus_raw(pc) + ic.f2_sminus_raw(pc)) / (
            ic.M2splus(pc) + ic.M2sminus(pc)
        )

    #  f1hat["yad"] = f1hat.apply(yadf1tilde, axis=1)
    #  f2hat["yad"] = f2hat.apply(yadf2tilde, axis=1)
    f1hat.reset_index(drop=True, inplace=True)
    f2hat.reset_index(drop=True, inplace=True)
    f1tilde.reset_index(drop=True, inplace=True)
    f2tilde.reset_index(drop=True, inplace=True)

    def apf_ratio(n1, n2):
        assert f2hat["Q2"][n1] == f2hat["Q2"][n2]
        f2 = f2hat["apf"]
        f1 = f1hat["apf"]
        return (f2[n1] / f1[n1]) / (f2[n2] / f1[n2])

    def yad_ratio(n1, n2):
        assert f2hat["Q2"][n1] == f2hat["Q2"][n2]
        f2z1 = yadf2tilde(f2hat.iloc[n1])
        f1z1 = yadf1tilde(f1hat.iloc[n1])
        f2z2 = yadf2tilde(f2hat.iloc[n2])
        f1z2 = yadf1tilde(f1hat.iloc[n2])
        #  return (f2[n1] / f1[n1]) / (f2[n2] / f1[n2])
        return (f2z1 / f1z1) / (f2z2 / f1z2)

    def ratio(start, diff):
        n1 = start
        n2 = start + diff
        print(
            f"z1: {f2hat['z'][n1]:.3e} - z2: {f2hat['z'][n2]:.3e} --- Q2: {f2hat['Q2'][n1]:.3f}"
        )
        print("apf:", apf_ratio(n1, n2))
        print("yad:", yad_ratio(n1, n2))

    start = 0
    diff = 0
    ratio(start, diff)
    for diff in [2, 4, 6]:
        print(f"\n\t--- diff {diff} scan ---")
        for start in range(4029, 9999, 712):
            ratio(start, diff)

    for start in [3000, 5120, 8150]:
        print(f"\n\t--- start {start} scan ---")
        for diff in range(1, 10):
            ratio(start, diff)

    pdb.set_trace()
    f1tilde["yad"] = f1tilde.apply(yadf1tilde, axis=1)
    f2tilde["yad"] = f2tilde.apply(yadf2tilde, axis=1)
    f1tilde["ratio"] = f1tilde["yad"] / f1tilde["apf"]
    f2tilde["ratio"] = f2tilde["yad"] / f2tilde["apf"]
    pdb.set_trace()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apfel", action="store_true")
    parser.add_argument("--hard", action="store_true")
    parser.add_argument("--soft", action="store_true")
    parser.add_argument("--soft1", action="store_true")
    args = parser.parse_args()

    if args.apfel:
        call_apfel()
    elif args.hard:
        analyze_fhat()
    elif args.soft:
        analyze_soft()
    elif args.soft1:
        analyze_soft1()
    else:
        analyze_soft1()
