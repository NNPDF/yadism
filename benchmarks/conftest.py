import sys
import pathlib
import itertools
import datetime

import numpy as np
import pandas as pd
import tinydb
import pytest

import lhapdf

from yadism.runner import Runner

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
import toyLH  # pylint:disable=import-error,wrong-import-position
from apfel_utils import ( # pylint:disable=import-error,wrong-import-position
    get_apfel_data,
    str_datetime,
)

class DBInterface:
    """
        Interface to access DB
    """
    def __init__(self, obs_table_name = "observables"):
        self._inputdb = tinydb.TinyDB(here / "data" / "input.json")
        self._obs_table_name = obs_table_name
        self._outputdb = tinydb.TinyDB(here / "data" / "output.json")
        self.theory_query = tinydb.Query()
        self.obs_query = tinydb.Query()

    def _load_input(self, theory_query, obs_query):
        theories = self._inputdb.table("theories").search(theory_query)
        observables = self._inputdb.table(self._obs_table_name).search(obs_query)
        return theories, observables

    def run_queries_regression(self, theory_query, obs_query):
        theories, observables = self._load_input(theory_query,obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_regression(theory, obs)

    def run_regression(self, theory, obs):
        pass

    def run_all_against_apfel(self, theory_query, obs_query, pdfs):
        theories, observables = self._load_input(theory_query,obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_against_apfel(theory, obs, pdfs)

    def _get_output_comparison(self, theory, observables, yad_tab, apf_tab, other_name, do_assert=False):
        log_tab = {}
        # loop kinematics
        for sf in yad_tab:
            kinematics = []
            for yad, apf in zip(yad_tab[sf], apf_tab[sf]):
                # check kinematics
                if any([yad[k] != apf[k] for k in ["x", "Q2"]]):
                    raise ValueError("Sort problem: x and/or Q2 do not match.")
                # extract values
                kin = dict(x=yad["x"], Q2=yad["Q2"])

                # refactor from here --->8---->8----
                kin[other_name] = ref = apf["value"]
                kin["yadism"] = fx = yad["result"]
                kin["yadism_error"] = err = yad["error"]
                # do hard test?
                if do_assert:
                    # TODO: find a solution that works down to more than 1e-6
                    assert pytest.approx(ref, rel=0.01, abs=max(err, 1e-6)) == fx
                # compare for log
                with np.errstate(divide="ignore"):
                    comparison = (fx / np.array(ref) - 1.0) * 100
                kin["rel_err[%]"] = comparison
                # to here --------->8---->8----->8--->8

                kinematics.append(kin)
            log_tab[sf] = kinematics

        # add metadata to log record
        log_tab["_creation_time"] = str_datetime(datetime.datetime.now())
        log_tab["_theory_doc_id"] = theory.doc_id
        log_tab["_observables_doc_id"] = observables.doc_id
        return log_tab

    def run_against_apfel(self, theory, observables, pdfs):
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
            observables_f :
                file path for the observables runcard
        """

        # ======================
        # get observables values
        # ======================
        runner = Runner(theory, observables)
        for pdf_name in pdfs:

            # setup PDFset
            if pdf_name == "ToyLH":
                pdf = toyLH.mkPDF("ToyLH", 0)
            else:
                pdf = lhapdf.mkPDF(pdf_name, 0)
            # run codes
            yad_tab = runner.apply(pdf)
            apf_tab = get_apfel_data(
                theory, observables, pdf_name, self._outputdb.table("apfel_cache")
            )

            # collect and check results
            log_tab = self._get_output_comparison(theory,observables,yad_tab,apf_tab,"APFEL")

            # =============
            # print and log
            # =============
            log_tab["_pdf"] = pdf_name
            # print immediately
            self._print_res(log_tab)
            # store the log
            self._log(log_tab)

    def _print_res(self, log_tab):
        # for each observable:
        for FX, tab in log_tab.items():
            # skip metadata
            if FX[0] == "_":
                continue

            print_tab = pd.DataFrame(tab)

            # print results
            print(f"\n---{FX}---\n")
            print(print_tab)
            print("\n--------\n")

    def _log(self, log_tab):
        """
            Dump comparison table.

            Parameters
            ----------
            log_tab :
                dict of lists of dicts, to be printed and saved in multiple csv
                files
        """

        # store the log of results
        self._outputdb.table("logs").insert(log_tab)

    def empty_cache(self):
        self._inputdb.table("apfel_cache").purge()
