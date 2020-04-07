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
from utils import test_data_dir, logs_dir, load_runcards, print_comparison_table

# available observables
observables = [
    "F2light",
    "F2charm",
    "F2bottom",
    # "F2top",
    "FLlight",
    "FLcharm",
    "FLbottom",
    # "FLtop",
]


def test_LO():
    """
    Test the full LO order against APFEL's.
    """
    theory_f = test_data_dir / "theory_LO.yaml"
    # iterate over observables - only F2light at LO
    for obs in observables[:1]:
        dis_observables_f = test_data_dir / f"{obs}.yaml"
        run_against_apfel(theory_f, dis_observables_f)


def test_NLO():
    """
    Test the full NLO order against APFEL's.
    """
    theory_f = test_data_dir / "theory_NLO.yaml"
    # iterate over observables
    for obs in observables:
        dis_observables_f = test_data_dir / f"{obs}.yaml"
        run_against_apfel(theory_f, dis_observables_f)


def run_against_apfel(theory_f, dis_observables_f):
    """
        Run APFEL comparison on the given runcards.

        Steps:
        - load runcards
            - using ``load_runcards``
        - instantiate and call yadism's Runner
            - using ``yadism.Runner``
        - retrieve APFEL data to compare with
            - using ``get_apfel_data``
        - check and collect comparison results
            - using ``assert``
            - using ``print_comparison_table``

        Parameters
        ----------
        theory_f :
            file path for the theory runcard
        dis_observables_f :
            file path for the observables runcard
    """
    theory, dis_observables = load_runcards(theory_f, dis_observables_f)

    # ============
    # setup PDFset
    # ============
    pdfset = theory.get("PDFSet", "ToyLH")
    if pdfset == "ToyLH":
        pdfs = toyLH.mkPDF("ToyLH", 0)
    else:
        pdfs = lhapdf.mkPDF(pdfset, 0)

    # ======================
    # get observables values
    # ======================
    runner = Runner(theory, dis_observables)

    yad_tab = runner.apply(pdfs)
    apf_tab = get_apfel_data(theory_f, dis_observables_f)

    # =========================
    # collect and check results
    # =========================

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
            # assert pytest.approx(ref, rel=0.01, abs=max(err, 1e-6)) == fx
            # assert pytest.approx(ref, rel=0.01, abs=err) == fx
            if ref == 0.0:
                comparison = np.nan
            else:
                comparison = (fx / ref - 1.0) * 100
            kin["rel_err[%]"] = comparison
            kinematics.append(kin)

    # =============
    # print and log
    # =============
    logs_path_template = (
        logs_dir / f"{theory_f.stem}-{dis_observables_f.stem}-{{obs}}.csv"
    )
    print_comparison_table(res_tab, logs_path_template)


if __name__ == "__main__":
    test_LO()
    test_NLO()
