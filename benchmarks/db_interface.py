import sys
import pathlib
import itertools
import datetime

import numpy as np
import pandas as pd
import tinydb
import pytest

from yadism.runner import Runner

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
import toyLH  # pylint:disable=import-error,wrong-import-position
from apfel_utils import str_datetime  # pylint:disable=import-error,wrong-import-position


class DBInterface:
    """
        Interface to access DB
    """

    def __init__(self, db_name):
        self._db = tinydb.TinyDB(here / "data" / db_name)
        self.theory_query = tinydb.Query()
        self.obs_query = tinydb.Query()

    def _load_input(self, theory_query, obs_query):
        theories = self._db.table("theories").search(theory_query)
        observables = self._db.table("observables").search(
            obs_query
        )
        return theories, observables

    def run_queries_regression(self, theory_query, obs_query):
        theories, observables = self._load_input(theory_query, obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_regression(theory, obs)

    def run_queries_apfel(self, theory_query, obs_query, pdfs):
        theories, observables = self._load_input(theory_query, obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_apfel(theory, obs, pdfs)

    def run_apfel(self, theory, observables, pdfs):
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
        from apfel_utils import get_apfel_data  # pylint:disable=import-error,import-outside-toplevel

        # ======================
        # get observables values
        # ======================
        runner = Runner(theory, observables)
        for pdf_name in pdfs:

            # setup PDFset
            if pdf_name == "ToyLH":
                pdf = toyLH.mkPDF("ToyLH", 0)
            else:
                import lhapdf # pylint:disable=import-outside-toplevel
                pdf = lhapdf.mkPDF(pdf_name, 0)
            # run codes
            yad_tab = runner.apply(pdf)
            apf_tab = get_apfel_data(
                theory, observables, pdf_name, self._db.table("apfel_cache")
            )

            # collect and check results
            log_tab = self._get_output_comparison(
                theory, observables, yad_tab, apf_tab, self._process_APFEL_log
            )

            # =============
            # print and log
            # =============
            log_tab["_pdf"] = pdf_name
            # print immediately
            self._print_res(log_tab)
            # store the log
            self._log(log_tab)

    def run_generate_regression(self, theory_query, obs_query):
        ask = input("Regenerate regression data? [y/n]")
        if ask != "y":
            print("Nothing done.")
            return
        theories, observables = self._load_input(theory_query, obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.generate_regression(theory, obs)

    def generate_regression(self, theory, obs):
        runner = Runner(theory, obs)
        out = runner.get_output()
        # add metadata to log record
        out["_creation_time"] = str_datetime(datetime.datetime.now())
        out["_theory_doc_id"] = theory.doc_id
        out["_observables_doc_id"] = obs.doc_id
        # check existence
        q = tinydb.Query()
        query = (q._theory_doc_id == theory.doc_id) & (
            q._observables_doc_id == obs.doc_id
        )
        regression_log = self._db.table("regressions").search(query)
        if len(regression_log) != 0:
            raise RuntimeError(
                f"there is already a document for t={theory.doc_id} and o={obs.doc_id}"
            )
        # insert
        self._db.table("regressions").insert(out)

    def run_regression(self, theory, obs):
        runner = Runner(theory, obs)
        out = runner.get_output()
        # load regression data
        q = tinydb.Query()
        query = (q._theory_doc_id == theory.doc_id) & (
            q._observables_doc_id == obs.doc_id
        )
        regression_log = self._db.table("regressions").search(query)
        if len(regression_log) == 0:
            raise RuntimeError(
                "no regression data to compare to! you need to generate first ..."
            )
        if len(regression_log) > 1:
            raise RuntimeError(
                f"there is more then one document for t={theory.doc_id} and o={obs.doc_id}"
            )
        regression_log = regression_log[0]
        # compare
        log_tab = self._get_output_comparison(
            theory, obs, out, regression_log, self._process_regression_log
        )
        # print immediately
        # self._print_res(log_tab)
        # store the log
        self._log(log_tab)

    @staticmethod
    def _process_APFEL_log(yad, apf):
        kin = dict()
        kin["APFEL"] = ref = apf["value"]
        kin["yadism"] = fx = yad["result"]
        kin["yadism_error"] = yad["error"]
        # compare for log
        with np.errstate(divide="ignore",invalid="ignore"):
            comparison = (fx / np.array(ref) - 1.0) * 100
        kin["rel_err[%]"] = comparison
        return kin

    @staticmethod
    def _process_regression_log(yad, reg):
        kin = dict()
        # iterate flavours
        for fl in ["q", "g"]:
            kin[f"reg {fl}"] = reg[fl]
            kin[f"reg {fl}_error"] = reg[f"{fl}_error"]
            kin[f"yad {fl}"] = yad[fl]
            kin[f"yad {fl}_error"] = yad[f"{fl}_error"]
            # do hard test?
            for f, r, e1, e2 in zip(
                yad[fl], reg[fl], yad[f"{fl}_error"], reg[f"{fl}_error"]
            ):
                assert pytest.approx(r, rel=0.01, abs=max(e1 + e2, 1e-6)) == f
            # compare for log
            with np.errstate(divide="ignore"):
                comparison = (np.array(yad[fl]) / np.array(reg[fl]) - 1.0) * 100
            kin[f"rel {fl}_err[%]"] = comparison.tolist()
        return kin

    def _get_output_comparison(
        self, theory, observables, yad_tab, other_tab, process_log
    ):
        log_tab = {}
        # loop kinematics
        for sf in yad_tab:
            # TODO make this more stable
            if sf[0] != "F":
                continue
            kinematics = []
            for yad, oth in zip(yad_tab[sf], other_tab[sf]):
                # check kinematics
                if any([yad[k] != oth[k] for k in ["x", "Q2"]]):
                    raise ValueError("Sort problem: x and/or Q2 do not match.")
                # extract values
                kin = process_log(yad, oth)
                # add common values
                kin["x"] = yad["x"]
                kin["Q2"] = yad["Q2"]
                kinematics.append(kin)
            log_tab[sf] = kinematics

        # add metadata to log record
        log_tab["_creation_time"] = str_datetime(datetime.datetime.now())
        log_tab["_theory_doc_id"] = theory.doc_id
        log_tab["_observables_doc_id"] = observables.doc_id
        return log_tab

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
        self._db.table("logs").insert(log_tab)

    def empty_cache(self):
        self._db.table("apfel_cache").purge()
