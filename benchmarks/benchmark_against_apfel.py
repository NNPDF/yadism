# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's
import sys
import os
import pathlib
import abc
import itertools

import numpy as np
import pandas as pd
import pytest
import tinydb
import lhapdf

from yadism.runner import Runner

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
import toyLH as toyLH
from apfel_utils import get_apfel_data


class ParentTest(abc.ABC):
    def __init__(self):
        self.__inputdb = tinydb.TinyDB(here / "data" / "input.json")
        self.__outputdb = tinydb.TinyDB(here / "data" / "output.json")
        self._theory_query = tinydb.Query()
        self._obs_query = tinydb.Query()

    def run_all_tests(self, theory_query, obs_query):
        theories = self.__inputdb.table("theories").search(theory_query)
        observables = self.__inputdb.table("dis_observables").search(obs_query)

        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_against_apfel(theory, obs)

    def run_against_apfel(self, theory, dis_observables):
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
        apf_tab = get_apfel_data(
            theory, dis_observables, self.__outputdb.table("apfel_cache")
        )

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
        res_tab["input_hash"] = apf_tab["input_hash"]
        self._print_res(res_tab)
        self._log(res_tab)

    def _print_res(self, res_tab):
        # for each observable:
        for FX, tab in res_tab.items():
            if len(tab) == 0 or FX == "input_hash":
                continue
            print_tab = pd.DataFrame(tab)

            # print results
            print(f"\n---{FX}---\n")
            print(print_tab)
            print("\n--------\n")

    def _log(self, res_tab):
        """
            Dump comparison table.

            Parameters
            ----------
            res_tab :
                dict of lists of dicts, to be printed and saved in multiple csv
                files
        """

        # store the log of results
        self.__outputdb.table("logs").insert(res_tab)


@pytest.mark.skip
class TestPlain:
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0
        t_query &= p._theory_query.PDFSet == "ToyLH"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0
        t_query &= p._theory_query.PDFSet == "ToyLH"

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)


@pytest.mark.skip
class TestScaleVariations:
    def test_LO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.PDFSet == "CT14llo_NF3"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.PDFSet == "CT14llo_NF3"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)


class TestFull:
    def test_LO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.PDFSet.one_of(["ToyLH", "CT14llo_NF3"])

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.PDFSet.one_of(["ToyLH", "CT14llo_NF3"])

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)


if __name__ == "__main__":
    plain = TestPlain()
    # plain.test_LO()
    # plain.test_NLO()

    sv = TestScaleVariations()
    # sv.test_LO()
    sv.test_NLO()
