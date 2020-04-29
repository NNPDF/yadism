import sys
import pathlib
import itertools
import datetime

import numpy as np
import pandas as pd
import tinydb
import lhapdf
import pytest

from yadism.runner import Runner

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
import toyLH as toyLH
from apfel_utils import get_apfel_data


class ParentTest:
    def __init__(self):
        self.__inputdb = tinydb.TinyDB(here / "data" / "input.json")
        self.__outputdb = tinydb.TinyDB(here / "data" / "output.json")
        self._theory_query = tinydb.Query()
        self._obs_query = tinydb.Query()

    def run_all_tests(self, theory_query, obs_query):
        theories = self.__inputdb.table("theories").search(theory_query)
        observables = self.__inputdb.table("observables").search(obs_query)

        for theory, obs in itertools.product(theories, observables):
            # run against apfel (test)
            self.run_against_apfel(theory, obs)

    def run_against_apfel(self, theory, observables):
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
        runner = Runner(theory, observables)

        yad_tab = runner.apply(pdfs)
        apf_tab = get_apfel_data(
            theory, observables, self.__outputdb.table("apfel_cache")
        )

        # =========================
        # collect and check results
        # =========================

        log_tab = {}
        # loop kinematics
        for sf in yad_tab:
            kinematics = log_tab[sf] = []
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
        # add metadata to log record
        log_tab["_creation_time"] = str(datetime.datetime.now())
        log_tab["_theory_doc_id"] = theory.doc_id
        log_tab["_observables_doc_id"] = observables.doc_id
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
        self.__outputdb.table("logs").insert(log_tab)

    def subtract_tables(self, id1, id2):
        """
            Subtract yadism and APFEL result in the second table from the first one,
            properly propagate the integration error and recompute the relative
            error on the subtracted results.

            Parameters
            ----------
            file1 :
                path for csv file with the table to subtract from
            file2 :
                path for csv file with the table to be subtracted
            output_f :
                path for csv file to store the result
        """

        msg = f"Subtracting id:{id1} - id:{id2}, in table 'logs'"
        print(msg, "=" * len(msg), sep="\n")
        print()

        # load json documents
        log1 = self.__outputdb.table("logs").get(doc_id=id1)
        log2 = self.__outputdb.table("logs").get(doc_id=id2)
        if log1 is None:
            raise ValueError(f"Log id:{id1} not found")
        elif log2 is None:
            raise ValueError(f"Log id:{id2} not found")

        for obs in log1.keys():
            if obs[0] == "_":
                continue
            elif obs not in log2:
                print(f"{obs}: not matching in log2")
                continue

            # load observable tables
            table1 = pd.DataFrame(log1[obs])
            table2 = pd.DataFrame(log2[obs])

            # check for compatible kinematics
            if any([any(table1[y] != table2[y]) for y in ["x", "Q2"]]):
                raise ValueError("Cannot compare tables with different (x, Q2)")

            # subtract and propagate
            table2["APFEL"] -= table1["APFEL"]
            table2["yadism"] -= table1["yadism"]
            table2["yadism_error"] += table1["yadism_error"]

            # compute relative error
            def rel_err(row):
                if row["APFEL"] == 0.0:
                    return np.nan
                else:
                    return (row["yadism"] / row["APFEL"] - 1.0) * 100

            table2["rel_err[%]"] = table2.apply(rel_err, axis=1)

            # dump results' table
            # with open(output_f, "w") as f:
            # table2.to_csv(f)
            print(obs, "-" * len(obs), sep="\n")
            print(table2)

    def empty_cache(self):
        self.__inputdb.table("apfel_cache").purge()


if __name__ == "__main__":
    p = ParentTest()
    p.subtract_tables(1, 2)
