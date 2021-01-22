# -*- coding: utf-8 -*-
import pandas as pd

from banana.data import sql, dfdict
from banana.benchmark.runner import BenchmarkRunner

from yadmark.banana_cfg import banana_cfg
from yadmark.data import observables

import yadism


class Runner(BenchmarkRunner):
    banana_cfg = banana_cfg

    @staticmethod
    def init_ocards(conn):
        with conn:
            conn.execute(sql.create_table("observables", observables.default_card))

    @staticmethod
    def load_ocards(conn, observables_updates, /):
        return observables.load(conn, observables_updates)

    def run_me(self, theory, observable, pdf, /):
        """
        Run yadism

        Parameters
        ----------
            theory : dict
                theory card
            observable : dict
                observable card
            pdf : lhapdf_like
                PDF set

        Returns
        -------
            out : yadism.output.Output
                yadism output
        """
        runner = yadism.Runner(theory, observable)
        return runner.apply_pdf(pdf)

    def run_external(self, theory, observable, pdf, /):

        if theory["IC"] != 0 and theory["PTO"] > 0:
                raise ValueError(f"{self.external} is currently not able to run")

        if self.external == "APFEL":
            from .external import (  # pylint:disable=import-error,import-outside-toplevel
                apfel_utils,
            )
            #if theory["IC"] != 0 and theory["PTO"] > 0:
            #    raise ValueError("APFEL is currently not able to run")
            return apfel_utils.compute_apfel_data(theory, observable, pdf)

        elif self.external == "QCDNUM":
            from .external import (  # pylint:disable=import-error,import-outside-toplevel
                qcdnum_utils,
            )
            return qcdnum_utils.compute_qcdnum_data(theory, observable, pdf)

        return {}

    def log(self, theory, ocard, pdf, me, ext, /):
        log_tab = dfdict.DFdict()
        for sf in me:
            if not yadism.observable_name.ObservableName.is_valid(sf):
                continue
            esfs = []
            
            for yad, oth in zip(me[sf], ext[sf]):
                # check kinematics
                if any([yad[k] != oth[k] for k in ["x", "Q2"]]):
                    raise ValueError("Sort problem: x and/or Q2 do not match.")
                # add common values
                esf = {}
                esf["x"] = yad["x"]
                esf["Q2"] = yad["Q2"]
                esf["yadism"] = f = yad["result"]
                esf["yadism_error"] = yad["error"]
                esf[self.external] = r = oth["result"]
                esf["percent_error"] = (f - r) / r * 100
                esfs.append(esf)
            log_tab[sf] = pd.DataFrame(esfs)
        return log_tab
