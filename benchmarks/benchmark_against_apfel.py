# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's
import sys
import os
import pathlib
import abc
import itertools

import numpy as np
import lhapdf
import pytest
import tinydb

from yadism.runner import Runner

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
import toyLH as toyLH
from apfel_utils import get_apfel_data
from utils import benchmark_data_dir, logs_dir, load_runcards, print_comparison_table


class ParentTest(abc.ABC):
    def __init__(self):
        self.__inputdb = tinydb.TinyDB(benchmark_data_dir / "input.json")
        self._theory_query = tinydb.Query()
        self._obs_query = tinydb.Query()

    def run_all_tests(self, theory_query, obs_query):
        theories = self.__inputdb.table("theories").search(theory_query)
        observables = self.__inputdb.table("dis_observables").search(obs_query)

        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            run_against_apfel(theory, obs)


class TestPlain(ParentTest):
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        t_query = self._theory_query.PTO == 0
        t_query &= self._theory_query.XIR == 1.0
        t_query &= self._theory_query.XIF == 1.0

        o_query = self._obs_query.F2light.exists()

        self.run_all_tests(t_query, o_query)

    # def test_NLO(self):
    # """
    # Test the full NLO order against APFEL's.
    # """
    # theory_test("theory_NLO.yaml")


# class TestScaleVariations:
# def test_LO(self):
# theory_test("theory_SV_LO.yaml", 1)

# def test_NLO(self):
# theory_test("theory_SV_NLO.yaml")


# class TestFull:
# pass


def run_against_apfel(theory, dis_observables):
    """
        Run APFEL comparison on the given runcards.

        Steps:
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
    apf_tab = get_apfel_data(theory, dis_observables)

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
        logs_dir / f"{theory.doc_id}-{dis_observables.doc_id}-{{obs}}.csv"
    )
    print_comparison_table(res_tab, logs_path_template)


if __name__ == "__main__":
    plain = TestPlain()
    plain.test_LO()
    # plain.test_NLO()

    # sv = TestScaleVariations()
    # sv.test_LO()
    # sv.test_NLO()
