# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's
import sys
import os
import pathlib

import yaml
import numpy as np
import lhapdf
import pytest

from yadism.runner import Runner

sys.path.append(os.path.join(os.path.dirname(__file__), "aux"))
import toyLH as toyLH
from apfel_utils import get_apfel_data


# def test_LO():
# theory, dis_observables = load_runcards("theory_LO.yaml", "dis_observables.yaml")
# run_against_apfel(theory, dis_observables)


def test_NLO():
    theory, dis_observables = load_runcards("theory_NLO.yaml", "dis_observables.yaml")
    run_against_apfel(theory, dis_observables)


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

    yad_tab = runner.apply(pdfs)
    apf_tab = get_apfel_data(theory, dis_observables)

    res_tab = {}
    # loop kinematics
    for sf in yad_tab:
        kinematics = res_tab[sf] = []
        for yad, apf in zip(yad_tab[sf], apf_tab[sf]):
            if any([yad[k] != apf[k] for k in ["x", "Q2"]]):
                raise ValueError("Sort problem")

            kin = dict(x=yad["x"], Q2=yad["Q2"])
            kin["APFEL"] = ref = apf["value"]
            kin["yadism"] = fx = yad["result"]
            kin["yadism_error"] = err = yad["error"]
            # TODO: find a solution that works down to more than 1e-6
            assert pytest.approx(ref, rel=0.01, abs=max(err, 1e-6)) == fx
            # assert pytest.approx(ref, rel=0.01, abs=err) == fx
            if ref == 0.0:
                comparison = np.nan
            else:
                comparison = (fx / ref - 1.0) * 100
            kin["rel_err[%]"] = comparison
            kinematics.append(kin)
    print_comparison_table(res_tab)


def print_comparison_table(res_tab):
    import pandas as pd

    for FX, tab in res_tab.items():
        if len(tab) == 0:
            continue
        print_tab = pd.DataFrame(tab)
        # print_tab.columns = ["x", "Q2", "APFEL", "yadism", "yadism_error", "rel_err[%]"]

        # print results
        print(f"\n---{FX}---\n")
        print(print_tab)
        print("\n--------\n")


if __name__ == "__main__":
    test_NLO()
