# -*- coding: utf-8 -*-
#
# Testing the loading functions
import sys
import os

# from pprint import pprint

import yaml
import numpy as np
import lhapdf
import pytest

from yadism.runner import Runner

sys.path.append(os.path.join(os.path.dirname(__file__), "aux"))
import toyLH as toyLH
from apfel_import import load_apfel


def test_loader():
    """Test the loading mechanism"""

    test_dir = os.path.dirname(__file__)
    # read files
    theory_file = os.path.join(test_dir, "data/theory_LO.yaml")
    with open(theory_file, "r") as file:
        theory = yaml.safe_load(file)
    observables_file = os.path.join(test_dir, "data/dis_observables.yaml")
    with open(observables_file, "r") as file:
        dis_observables = yaml.safe_load(file)

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

        assert pytest.approx(ref, rel=0.1) == f2_lo
        # res_tab.append([x, Q2, ref, f2_lo, ref / f2_lo])

    # # print results

    # print("\n------\n")
    # print("x", "Q2", "APFEL", "yadism", "ratio", sep="\t")
    # for x in res_tab:
    # for y in x:
    # print(y, "" if len(str(y)) > 7 else "\t", sep="", end="\t")
    # print()
    # print("\n------\n")


if __name__ == "__main__":
    test_loader()
