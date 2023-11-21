"""Localized implementation of BenchmarkRunner."""
import numpy as np
import pandas as pd
from banana.benchmark.runner import BenchmarkRunner
from banana.data import dfdict
from eko.couplings import Couplings, couplings_mod_ev
from eko.io import dictlike, runcards, types
from eko.matchings import Atlas, nf_default
from eko.quantities.heavy_quarks import MatchingScales

import yadism
from yadmark.data import db, observables


class Runner(BenchmarkRunner):
    """Localized implementation of BenchmarkRunner."""

    alphas_from_lhapdf = False
    """Use the alpha_s routine provided by the Pdf?"""

    db_base_cls = db.Base

    @staticmethod
    def load_ocards(conn, ocard_updates):
        """Load observable cards."""
        return observables.load(conn, ocard_updates)

    def run_me(self, theory, ocard, pdf):
        """
        Run yadism.

        Parameters
        ----------
        theory : dict
            theory card
        ocard : dict
            observable card
        pdf : lhapdf_like
            PDF set

        Returns
        -------
        out : yadism.output.PDFOutput
            yadism output

        """
        runner = yadism.Runner(theory, ocard)
        # choose alpha_s source
        if self.alphas_from_lhapdf:
            import lhapdf  # pylint:disable=E0401,C0415

            alpha_s = lambda muR: lhapdf.mkAlphaS(pdf.set().name).alphasQ(muR)
        else:
            new_eko_theory = runcards.Legacy(theory=theory, operator={}).new_theory
            method = runcards.Legacy.MOD_EV2METHOD.get(theory["ModEv"], theory["ModEv"])
            method = dictlike.load_enum(types.EvolutionMethod, method)
            method = couplings_mod_ev(method)
            masses = [mq**2 for mq, _ in new_eko_theory.heavy.masses]
            thresholds_ratios = np.power(new_eko_theory.heavy.matching_ratios, 2)
            sc = Couplings(
                couplings=new_eko_theory.couplings,
                order=new_eko_theory.order,
                method=method,
                masses=masses,
                hqm_scheme=new_eko_theory.heavy.masses_scheme,
                thresholds_ratios=thresholds_ratios.tolist(),
            )
            atlas = Atlas(
                matching_scales=MatchingScales(masses * thresholds_ratios),
                origin=(theory["Qref"] ** 2, theory["nfref"]),
            )
            alpha_s = (
                lambda muR: sc.a_s(muR**2, nf_to=nf_default(muR**2, atlas))
                * 4.0
                * np.pi
            )

        alpha_qed = lambda _muR: theory["alphaqed"]
        return runner.get_result().apply_pdf_alphas_alphaqed_xir_xif(
            pdf, alpha_s, alpha_qed, theory["XIR"], theory["XIF"]
        )

    def run_external(self, theory, ocard, pdf):
        """
        Run external.

        Parameters
        ----------
        theory : dict
            theory card
        ocard : dict
            observable card
        pdf : lhapdf_like
            PDF set

        Returns
        -------
        dict
            external output

        """
        observable = ocard

        if self.external.upper() == "APFEL":
            from .external import (  # pylint:disable=import-error,import-outside-toplevel
                apfel_utils,
            )

            return apfel_utils.compute_apfel_data(theory, observable, pdf)

        elif self.external.upper() == "QCDNUM":
            from .external import (  # pylint:disable=import-error,import-outside-toplevel
                qcdnum_utils,
            )

            return qcdnum_utils.compute_qcdnum_data(theory, observable, pdf)

        elif self.external.lower() == "xspace_bench":
            from .external import (  # pylint:disable=import-error,import-outside-toplevel
                xspace_bench_utils,
            )

            return xspace_bench_utils.compute_xspace_bench_data(theory, observable, pdf)

        elif self.external.upper() == "APFEL++":
            from .external import apfelpy_utils

            return apfelpy_utils.compute_apfelpy_data(theory, observable, pdf)

        elif self.external.lower() == "void":
            # set all ESF simply to 0
            res = {}
            for sf, esfs in ocard["observables"].items():
                if not yadism.observable_name.ObservableName.is_valid(sf):
                    continue
                void_esfs = []
                for esf in esfs:
                    n = esf.copy()
                    n.update({"result": 0})
                    void_esfs.append(n)
                res[sf] = void_esfs
            return res
        raise ValueError("Unknown external")

    def log(self, t, o, _pdf, me, ext):
        """Write log."""
        log_tab = dfdict.DFdict()
        kins = ["x", "Q2"]

        for sf in me:
            if not yadism.observable_name.ObservableName.is_valid(sf):
                continue
            esfs = []

            obs_kins = kins.copy()

            # skip if it is empty
            if len(me[sf]) == 0:
                continue

            if "y" in me[sf][0]:
                obs_kins += ["y"]

            # Sort the point using yadism order since yadism list can be different from ext
            for yad in me[sf]:
                cnt = 0
                for oth in ext[sf]:
                    if all([yad[k] == oth[k] for k in obs_kins]):
                        # add common values
                        esf = {}
                        esf["x"] = yad["x"]
                        esf["Q2"] = yad["Q2"]
                        if "y" in obs_kins:
                            esf["y"] = yad["y"]
                        esf["yadism"] = f = yad["result"]
                        esf["yadism_error"] = yad["error"]
                        esf[self.external] = r = oth["result"]
                        esf["percent_error"] = (f - r) / r * 100
                        esfs.append(esf)
                        cnt = 1
                        break
                if cnt == 0:
                    raise ValueError("Sort problem: x and/or Q2 do not match.")
            log_tab[sf] = pd.DataFrame(esfs)

        return log_tab
