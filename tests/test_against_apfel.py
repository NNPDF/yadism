# -*- coding: utf-8 -*-
#
# Testing the loading functions
import sys
import os
import pathlib

# from pprint import pprint

import yaml
import numpy as np
import lhapdf
import pytest

from yadism.runner import Runner

sys.path.append(os.path.join(os.path.dirname(__file__), "aux"))
import toyLH as toyLH
from apfel_import import load_apfel


def test_LO():
    theory, dis_observables = load_runcards("theory_LO.yaml", "dis_observables.yaml")
    run_against_apfel(theory, dis_observables)


# def test_NLO():
# theory, dis_observables = load_runcards("theory_NLO.yaml", "dis_observables.yaml")
# run_against_apfel(theory, dis_observables)


def load_runcards(theory_filename, observables_filename):
    """Test the loading mechanism"""

    test_data_dir = pathlib.Path(__file__).parent / "data"
    # read files
    # theory
    theory_file = test_data_dir / theory_filename
    with open(theory_file, "r") as f:
        theory = yaml.safe_load(f)
    # observables
    observables_file = test_data_dir / observables_filename
    with open(observables_file, "r") as f:
        dis_observables = yaml.safe_load(f)

    return theory, dis_observables


def run_against_apfel(theory, dis_observables):
    # =====================
    # execute DIS
    runner = Runner(theory, dis_observables)
    # =====================

    # setup LHAPDF
    pdfset = theory.get("PDFSet", "ToyLH")
    if pdfset == "ToyLH":
        pdfs = toyLH.mkPDF("ToyLH", 0)
    else:
        pdfs = lhapdf.mkPDF(pdfset, 0)

    result = runner.apply(pdfs)

    # setup APFEL
    apfel = load_apfel(theory)
    # loop kinematics
    res_tab = []

    for kinematics in result.get("F2", []):
        Q2 = kinematics["Q2"]
        x = kinematics["x"]
        # compute F2
        f2_lo = kinematics["result"]
        # execute APFEL (if needed)
        if False:
            pass
        else:
            apfel.ComputeStructureFunctionsAPFEL(np.sqrt(Q2), np.sqrt(Q2))
            ref = apfel.F2light(x)

        # assert pytest.approx(ref, rel=0.1) == f2_lo
        res_tab.append([x, Q2, ref, f2_lo, ref / f2_lo])

    print_comparison_table(res_tab)


def print_comparison_table(res_tab):
    # print results

    print("\n------\n")
    print("x", "Q2", "APFEL", "yadism", "ratio", sep="\t")
    for x in res_tab:
        for y in x:
            print(y, "" if len(str(y)) > 7 else "\t", sep="", end="\t")
        print()
    print("\n------\n")


if __name__ == "__main__":
    test_loader()
