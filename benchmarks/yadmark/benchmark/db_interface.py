# # -*- coding: utf-8 -*-


# class DBInterface(mode_selector.ModeSelector):


#     def run_queries_external(self, theory_query, obs_query, pdfs):
#         """
#         Run a test matrix for the external program
#         """
#         theories, observables = self._load_input_from_queries(theory_query, obs_query)
#         full = itertools.product(theories, observables)
#         # for theory, obs in rich.progress.track(
#         #     full, total=len(theories) * len(observables)
#         # ):
#         for theory, obs in full:
#             # create our own object
#             runner = Runner(theory, obs)
#             for pdf_name in pdfs:
#                 # setup PDFset
#                 if pdf_name == "ToyLH":
#                     pdf = toy.mkPDF("ToyLH", 0)
#                 else:
#                     import lhapdf  # pylint:disable=import-outside-toplevel

#                     # is the set installed? if not do it now
#                     if pdf_name not in lhapdf.availablePDFSets():
#                         print(f"PDFSet {pdf_name} is not installed! Installing now ...")
#                         subprocess.run(["lhapdf", "get", pdf_name], check=True)
#                         print(f"{pdf_name} installed.")
#                     pdf = lhapdf.mkPDF(pdf_name, 0)
#                 # get our data
#                 yad_tab = runner.apply_pdf(pdf)
#                 # get external data
#                 if self.external == "APFEL":
#                     from .external import (  # pylint:disable=import-error,import-outside-toplevel
#                         apfel_utils,
#                     )

#                     if theory["IC"] != 0 and theory["PTO"] > 0:
#                         print(yad_tab)
#                         raise ValueError("APFEL is currently not able to run")
#                     ext_tab = external.get_external_data(
#                         theory,
#                         obs,
#                         pdf,
#                         self.idb.table("apfel_cache"),
#                         apfel_utils.compute_apfel_data,
#                     )
#                 elif self.external == "QCDNUM":
#                     from .external import (  # pylint:disable=import-error,import-outside-toplevel
#                         qcdnum_utils,
#                     )

#                     ext_tab = external.get_external_data(
#                         theory,
#                         obs,
#                         pdf,
#                         self.idb.table("qcdnum_cache"),
#                         qcdnum_utils.compute_qcdnum_data,
#                     )
#                 else:
#                     raise ValueError(f"Unknown external {self.external}")

#                 # collect and check results
#                 log_tab = self._get_output_comparison(
#                     theory,
#                     obs,
#                     yad_tab,
#                     ext_tab,
#                     self._process_external_log,
#                     self.external,
#                     self.assert_external,
#                 )

#                 # =============
#                 # print and log
#                 # =============
#                 log_tab["_pdf"] = pdf_name
#                 # print immediately
#                 self._print_res(log_tab)
#                 # store the log
#                 self._log(log_tab)

#     @staticmethod
#     def _process_external_log(yad, apf, external, assert_external):
#         """
#         Post-process the output log.
#         """
#         kin = dict()
#         kin[external] = ref = apf["value"]
#         kin["yadism"] = fx = yad["result"]
#         kin["yadism_error"] = err = yad["error"]
#         # test equality
#         if assert_external is not False:
#             if not isinstance(assert_external, dict):
#                 assert_external = {}
#             assert (
#                 pytest.approx(
#                     ref,
#                     rel=assert_external.get("rel", 0.01),
#                     abs=max(err, assert_external.get("abs", 1e-6)),
#                 )
#                 == fx
#             )
#         # compare for log
#         with np.errstate(divide="ignore", invalid="ignore"):
#             comparison = (fx / np.array(ref) - 1.0) * 100
#         kin["rel_err[%]"] = comparison
#         return kin

#     def _get_output_comparison(
#         self,
#         theory,
#         observables,
#         yad_tab,
#         other_tab,
#         process_log,
#         external=None,
#         assert_external=None,
#     ):
#         rich.print(rich.markdown.Markdown("## Reporting results"))

#         log_tab = {}
#         # add metadata to log record
#         rich.print(
#             f"comparing for theory=[b]{theory.doc_id}[/b] and "
#             f"obs=[b]{observables.doc_id}[/b] ..."
#         )
#         log_tab["_created"] = datetime.datetime.now().isoformat()
#         log_tab["_theory_doc_id"] = theory.doc_id
#         log_tab["_observables_doc_id"] = observables.doc_id
#         if isinstance(yad_tab, Exception):
#             log_tab["_crash"] = yad_tab
#             return log_tab
#         # loop kinematics
#         for sf in yad_tab:
#             if not observable_name.ObservableName.is_valid(sf):
#                 continue
#             kinematics = []
#             for yad, oth in zip(yad_tab[sf], other_tab[sf]):
#                 # check kinematics
#                 if any([yad[k] != oth[k] for k in ["x", "Q2"]]):
#                     raise ValueError("Sort problem: x and/or Q2 do not match.")
#                 # add common values
#                 kin = {}
#                 kin["x"] = yad["x"]
#                 kin["Q2"] = yad["Q2"]
#                 # preprocess assertion contraints
#                 if callable(assert_external):
#                     assert_external_dict = assert_external(theory, observables, sf, yad)
#                 else:
#                     assert_external_dict = assert_external
#                 # run actual comparison
#                 try:
#                     kin.update(process_log(yad, oth, external, assert_external_dict))
#                 except AssertionError as e:
#                     log_tab["_crash"] = e
#                     log_tab["_crash_sf"] = sf
#                     log_tab["_crash_kin"] = kin
#                     log_tab["_crash_yadism"] = yad
#                     log_tab["_crash_other"] = oth
#                     log_tab["_crash_external"] = external
#                     log_tab["_crash_assert_rule"] = assert_external_dict
#                     # __import__("pdb").set_trace()
#                     return log_tab
#                 kinematics.append(kin)
#             log_tab[sf] = kinematics

#         return log_tab

#     def _print_res(self, log_tab):
#         # for each observable:
#         for FX, tab in log_tab.items():
#             # skip metadata
#             if FX[0] == "_":
#                 continue

#             print_tab = pd.DataFrame(tab)
#             length = len(str(print_tab).split("\n")[1])
#             rl = (length - len(FX)) // 2  # reduced length

#             # print results
#             rich.print("\n" + "-" * rl + f"[green i]{FX}[/]" + "-" * rl + "\n")
#             # __import__("pdb").set_trace()
#             rich.print(print_tab)
#             rich.print("-" * length + "\n\n")
