# -*- coding: utf-8 -*-
import itertools
import datetime
import copy

import numpy as np
import pandas as pd
import tinydb
import pytest

import rich
import rich.box
import rich.panel
import rich.progress
import rich.markdown

from yadism.runner import Runner
from yadism import observable_name

from .. import toyLH
from .. import utils
from .. import mode_selector
from . import external


class QueryFieldsEqual(tinydb.queries.QueryInstance):
    """
        Tests that two fields of the document are equal to each other

        Parameters
        ----------
            field_a : str
                first field
            field_b : str
                second field
    """

    def __init__(self, field_a, field_b):
        def test(doc):
            return field_a in doc and field_b in doc and doc[field_a] == doc[field_b]

        super().__init__(test, ("==", (field_a,), (field_b,)))


class DBInterface(mode_selector.ModeSelector):
    """
        Interface to access DB

        Parameters
        ----------
            external : str
                program to compare to
            db_name : str
                database name (relative to data/ directory)
    """

    def __init__(self, mode, external=None, assert_external=None):
        super(DBInterface, self).__init__(mode, external)
        self.assert_external = assert_external

        self.theory_query = tinydb.Query()
        self.obs_query = tinydb.Query()

        self.defaults = {
            "XIR": self.theory_query.XIR == 1.0,
            "XIF": self.theory_query.XIF == 1.0,
            "NfFF": self.theory_query.NfFF == 3,
            "FNS": self.theory_query.FNS == "FFNS",
            "DAMP": self.theory_query.DAMP == 0,
            "TMC": self.theory_query.TMC == 0,
        }

    def _load_input_from_queries(self, theory_query, obs_query):
        """
        Retrieve (JSON) data form the DB using the queries
        """
        theories = self.idb.table("theories").search(theory_query)
        observables = self.idb.table("observables").search(obs_query)
        rich.print(
            rich.panel.Panel.fit(
                f" Theories: {len(theories)}\n" f" Observables: {len(observables)}",
                rich.box.HORIZONTALS,
            )
        )
        return theories, observables

    def run_queries_regression(self, theory_query, obs_query):
        """
        Do the regression test.
        """
        theories, observables = self._load_input_from_queries(theory_query, obs_query)
        for theory, obs in itertools.product(theories, observables):
            # run against regression data
            self.run_regression(theory, obs)

    def run_generate_regression(self, theory_query, obs_query):
        """
        Regenerates the regression data.
        """
        # ask = input("Regenerate regression data? [y/n]")
        # if ask != "y":
        #    print("Nothing done.")
        #    return
        self.idb.table("regressions").truncate()
        theories, observables = self._load_input_from_queries(theory_query, obs_query)
        full = itertools.product(theories, observables)
        for theory, obs in rich.progress.track(
            full, total=len(theories) * len(observables)
        ):
            self.generate_regression(theory, obs)

    def generate_regression(self, theory, obs):
        """
        Generates a single regression point.
        """
        runner = Runner(theory, obs)
        out = runner.get_output()
        # add metadata to log record
        out["_creation_time"] = utils.str_datetime(datetime.datetime.now())
        out["_theory_doc_id"] = theory.doc_id
        out["_observables_doc_id"] = obs.doc_id
        # check existence
        q = tinydb.Query()
        query = (q._theory_doc_id == theory.doc_id) & (
            q._observables_doc_id == obs.doc_id
        )
        regression_log = self.idb.table("regressions").search(query)
        if len(regression_log) != 0:
            raise RuntimeError(
                f"there is already a document for t={theory.doc_id} and o={obs.doc_id}"
            )
        # insert
        self.idb.table("regressions").insert(out)

    def run_regression(self, theory, obs):
        """
        Run a single regression point.
        """
        runner = Runner(theory, obs)
        try:
            out = runner.get_output()
        except Exception as e:
            out = e
        # load regression data
        q = tinydb.Query()
        query = (q._theory_doc_id == theory.doc_id) & (
            q._observables_doc_id == obs.doc_id
        )
        regression_log = self.idb.table("regressions").search(query)
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

    def run_external(self, PTO, pdfs, theory_update=None, obs_query=None):
        # add PTO and build theory query
        if theory_update is None:
            theory_update = {}
        theory_update["PTO"] = self.theory_query.PTO == PTO
        theory = copy.deepcopy(self.defaults)
        theory.update(theory_update)
        theory_query = self.theory_query.noop()
        for cond in theory.values():
            # skip empty ones
            if cond is None:
                continue
            theory_query &= cond
        # build obs query
        if obs_query is None:
            obs_query = self.obs_query.prDIS.exists()
        return self.run_queries_external(theory_query, obs_query, pdfs)

    def run_queries_external(self, theory_query, obs_query, pdfs):
        theories, observables = self._load_input_from_queries(theory_query, obs_query)
        full = itertools.product(theories, observables)
        for theory, obs in rich.progress.track(
            full, total=len(theories) * len(observables)
        ):
            # create our own object
            runner = Runner(theory, obs)
            for pdf_name in pdfs:
                # setup PDFset
                if pdf_name == "ToyLH":
                    pdf = toyLH.mkPDF("ToyLH", 0)
                else:
                    import lhapdf  # pylint:disable=import-outside-toplevel

                    pdf = lhapdf.mkPDF(pdf_name, 0)
                # get our data
                yad_tab = runner.apply(pdf)
                # get external data
                if self.external == "APFEL":
                    from .external import (  # pylint:disable=import-error,import-outside-toplevel
                        apfel_utils,
                    )

                    ext_tab = external.get_external_data(
                        theory,
                        obs,
                        pdf,
                        self.idb.table("apfel_cache"),
                        apfel_utils.compute_apfel_data,
                    )
                elif self.external == "QCDNUM":
                    from .external import (  # pylint:disable=import-error,import-outside-toplevel
                        qcdnum_utils,
                    )

                    ext_tab = external.get_external_data(
                        theory,
                        obs,
                        pdf,
                        self.idb.table("qcdnum_cache"),
                        qcdnum_utils.compute_qcdnum_data,
                    )
                else:
                    raise ValueError(f"Unknown external {self.external}")

                # collect and check results
                log_tab = self._get_output_comparison(
                    theory,
                    obs,
                    yad_tab,
                    ext_tab,
                    self._process_external_log,
                    self.external,
                    self.assert_external,
                )

                # =============
                # print and log
                # =============
                log_tab["_pdf"] = pdf_name
                # print immediately
                self._print_res(log_tab)
                # store the log
                self._log(log_tab)

    @staticmethod
    def _process_external_log(yad, apf, external, assert_external):
        kin = dict()
        kin[external] = ref = apf["value"]
        kin["yadism"] = fx = yad["result"]
        kin["yadism_error"] = err = yad["error"]
        # test equality
        if assert_external is not False:
            if not isinstance(assert_external, dict):
                assert_external = {}
            assert (
                pytest.approx(
                    ref,
                    rel=assert_external.get("rel", 0.01),
                    abs=max(err, assert_external.get("abs", 1e-6)),
                )
                == fx
            )
        # compare for log
        with np.errstate(divide="ignore", invalid="ignore"):
            comparison = (fx / np.array(ref) - 1.0) * 100
        kin["rel_err[%]"] = comparison
        return kin

    @staticmethod
    def _process_regression_log(yad, reg, *_args):
        kin = dict()
        # iterate flavours
        for k in reg["values"]:
            kin[f"reg {k}"] = reg_val = reg["values"][k]
            kin[f"reg {k}_error"] = reg_err = reg["errors"][k]
            kin[f"reg {k}_weights"] = reg_weights = reg["weights"][k]
            kin[f"yad {k}"] = yad_val = yad["values"][k]
            kin[f"yad {k}_error"] = yad_err = yad["errors"][k]
            kin[f"yad {k}_weights"] = yad_weights = yad["weights"][k]

            # test equality
            for f, r, e1, e2 in zip(yad_val, reg_val, yad_err, reg_err):
                assert pytest.approx(r, rel=0.01, abs=max(e1 + e2, 1e-6)) == f
            # check weights
            reg_weights = {int(k): v for k, v in reg_weights.items()}
            assert pytest.approx(reg_weights) == yad_weights
            # compare for log
            with np.errstate(divide="ignore"):
                comparison = (np.array(yad_val) / np.array(reg_val) - 1.0) * 100
            kin[f"rel {k}_err[%]"] = comparison.tolist()
        return kin

    def _get_output_comparison(
        self,
        theory,
        observables,
        yad_tab,
        other_tab,
        process_log,
        external=None,
        assert_external=None,
    ):
        rich.print(rich.markdown.Markdown("## Reporting results"))

        log_tab = {}
        # add metadata to log record
        rich.print(
            f"comparing for theory=[b]{theory.doc_id}[/b] and "
            f"obs=[b]{observables.doc_id}[/b] ..."
        )
        log_tab["_creation_time"] = utils.str_datetime(datetime.datetime.now())
        log_tab["_theory_doc_id"] = theory.doc_id
        log_tab["_observables_doc_id"] = observables.doc_id
        if isinstance(yad_tab, Exception):
            log_tab["_crash"] = yad_tab
            return log_tab
        # loop kinematics
        for sf in yad_tab:
            if not observable_name.ObservableName.is_valid(sf):
                continue
            kinematics = []
            for yad, oth in zip(yad_tab[sf], other_tab[sf]):
                # check kinematics
                if any([yad[k] != oth[k] for k in ["x", "Q2"]]):
                    raise ValueError("Sort problem: x and/or Q2 do not match.")
                # add common values
                kin = {}
                kin["x"] = yad["x"]
                kin["Q2"] = yad["Q2"]
                # preprocess assertion contraints
                if callable(assert_external):
                    assert_external_dict = assert_external(theory, observables, sf, yad)
                else:
                    assert_external_dict = assert_external
                # run actual comparison
                try:
                    kin.update(process_log(yad, oth, external, assert_external_dict))
                except AssertionError as e:
                    log_tab["_crash"] = e
                    log_tab["_crash_sf"] = sf
                    log_tab["_crash_kin"] = kin
                    log_tab["_crash_yadism"] = yad
                    log_tab["_crash_other"] = oth
                    log_tab["_crash_external"] = external
                    log_tab["_crash_assert_rule"] = assert_external_dict
                    # __import__("pdb").set_trace()
                    return log_tab
                kinematics.append(kin)
            log_tab[sf] = kinematics

        return log_tab

    def _print_res(self, log_tab):
        # for each observable:
        for FX, tab in log_tab.items():
            # skip metadata
            if FX[0] == "_":
                continue

            print_tab = pd.DataFrame(tab)
            length = len(str(print_tab).split("\n")[1])
            rl = (length - len(FX)) // 2  # reduced length

            # print results
            rich.print("\n" + "-" * rl + f"[green i]{FX}[/]" + "-" * rl + "\n")
            # __import__("pdb").set_trace()
            rich.print(print_tab)
            rich.print("-" * length + "\n\n")

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
        crash_exception = log_tab.get("_crash", None)
        if crash_exception is not None:
            log_tab["_crash"] = str(type(crash_exception)) + ": " + str(crash_exception)
        new_id = self.odb.table("logs").insert(log_tab)
        rich.print(f"Added log with id={new_id}")
        # reraise exception if there is one
        if crash_exception is not None:
            raise crash_exception
