# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from banana import navigator as bnav
from banana.data import dfdict

from yadism import observable_name as on

from ..data import db

table_objects = bnav.table_objects
table_objects["o"] = db.Observable


class NavigatorApp(bnav.navigator.NavigatorApp):
    """
    Navigator base class holding all elementry operations.

    Parameters
    ----------
        cfg : dict
            banana configuration
        mode : string
            mode identifier
    """

    table_objects = table_objects

    def fill_theories(self, theo, obj):
        """
        Collect important information of the theory record.

        Parameters
        ----------
            theo : dict
                database record
            obj : dict
                to be updated pandas record
        """
        for f in ["PTO", "XIF", "XIR", "TMC", "NfFF", "FNS", "DAMP"]:
            obj[f] = theo[f]

    def fill_observables(self, ob, obj):
        """
        Collect important information of the observable record.

        Parameters
        ----------
            theo : dict
                database record
            obj : dict
                to be updated pandas record
        """
        if "PTO" in ob:
            obj["PTO"] = ob["PTO"]
        xgrid = ob["interpolation_xgrid"]
        obj["xgrid"] = (
            f"{len(xgrid)}pts: "
            + f"{'log' if ob['interpolation_is_log'] else 'x'}"
            + f"^{ob['interpolation_polynomial_degree']}"
        )
        obj["curr"] = ob["prDIS"]
        proj_map = {
            "electron": "e-",
            "positron": "e+",
            "neutrino": "ν",
            "antineutrino": "ν~",
        }
        obj["proj"] = proj_map[ob["ProjectileDIS"]]
        obj["pol"] = ob["PolarizationDIS"]
        sfs = 0
        esfs = 0
        for esfs_dict in ob["observables"].values():
            sfs += 1
            esfs += len(esfs_dict)
        obj["structure_functions"] = f"{sfs} SF @ {esfs} points"

    def fill_cache(self, cac, obj):
        """
        Collect important information of the cache record.

        Parameters
        ----------
            cac : dict
                database record
            obj : dict
                to be updated pandas record
        """
        for f in ["external", "pdf"]:
            obj[f] = cac[f]

        sfs = 0
        esfs = 0
        for esfs_dict in cac["result"].values():
            sfs += 1
            esfs += len(esfs_dict)

        obj["structure_functions"] = f"{sfs} SF @ {esfs} pts"

    def fill_logs(self, lg, obj):
        """
        Collect important information of the log record.

        Parameters
        ----------
            lg : dict
                database record
            obj : dict
                to be updated pandas record
        """
        sfs = 0
        esfs = 0
        for esfs_dict in lg["log"].values():
            sfs += 1
            esfs += len(esfs_dict)
        crash = lg.get("_crash", None)
        if crash is None:
            obj["structure_functions"] = f"{sfs} SF @ {esfs} pts"
        else:
            obj["structure_functions"] = crash
        obj["pdf"] = lg["pdf"]
        obj["external"] = lg["external"]

    def list_all_similar_logs(self, ref_hash):
        """
        Search logs which are similar to the one given, i.e., same theory and,
        same observable, and same pdfset.

        Parameters
        ----------
            ref_hash : hash
                partial hash of the reference log

        Returns
        -------
            df : pandas.DataFrame
                created frame

        Note
        ----
        The external it's not used to discriminate logs: even different
        externals should return the same numbers, so it's relevant to keep all
        of them.
        """
        # obtain reference log
        ref_log = self.get(bnav.l, ref_hash)

        related_logs = []
        all_logs = self.get(bnav.l)

        for lg in all_logs:
            if lg["t_hash"] != ref_log["t_hash"]:
                continue
            if lg["o_hash"] != ref_log["o_hash"]:
                continue
            if lg["pdf"] != ref_log["pdf"]:
                continue
            related_logs.append(lg)

        return self.list_all(bnav.l, related_logs)

    def log_as_dfd(self, doc_hash):
        """
        Load all structure functions in log as DataFrame

        Parameters
        ----------
            doc_hash : hash
                document hash

        Returns
        -------
            log : DFdict
                DataFrames
        """
        log = self.get(bnav.l, doc_hash)
        dfd = dfdict.DFdict()
        for sf in log["log"]:
            dfd.print(
                f"{sf} with theory={log['t_hash']}, "
                + f"obs={log['o_hash']} "
                + f"using {log['pdf']}"
            )
            dfd[sf] = pd.DataFrame(log["log"][sf])
        return dfd

    def subtract_tables(self, dfd1, dfd2):
        """
        Subtract results in the second table from the first one,
        properly propagate the integration error and recompute the relative
        error on the subtracted results.

        Parameters
        ----------
            dfd1 : dict or hash
                if hash the doc_hash of the log to be loaded
            dfd2 : dict or hash
                if hash the doc_hash of the log to be loaded

        Returns
        -------
            diffout : DFdict
                created frames
        """

        diffout = dfdict.DFdict()

        # load json documents
        logs = []
        ids = []
        for dfd in [dfd1, dfd2]:
            if isinstance(dfd, dfdict.DFdict):
                logs.append(dfd.to_document())
                ids.append("not-an-id")
            else:
                logs.append(self.log_as_dfd(dfd))
                ids.append(dfd)
        log1, log2 = logs
        id1, id2 = ids

        # print head
        msg = f"Subtracting id: '{id1}' - id: '{id2}', in table 'logs'"
        diffout.print(msg, "=" * len(msg), sep="\n")
        diffout.print()

        if log1 is None:
            raise ValueError(f"Log id: '{id1}' not found")
        if log2 is None:
            raise ValueError(f"Log id: '{id2}' not found")

        # iterate observables
        for obs in log1.keys():
            if obs[0] == "_":
                continue
            if obs not in log2:
                print(f"{obs}: not matching in log2")
                continue

            # load observable tables
            table1 = pd.DataFrame(log1[obs])
            table2 = pd.DataFrame(log2[obs])
            table_out = table2.copy()

            # check for compatible kinematics
            if any([any(table1[y] != table2[y]) for y in ["x", "Q2"]]):
                raise ValueError("Cannot compare tables with different (x, Q2)")

            # subtract and propagate
            known_col_set = set(["x", "Q2", "yadism", "yadism_error", "percent_error"])
            t1_ext = list(set(table1.keys()) - known_col_set)[0]
            t2_ext = list(set(table2.keys()) - known_col_set)[0]
            if t1_ext == t2_ext:
                tout_ext = t1_ext
            else:
                tout_ext = f"{t2_ext}-{t1_ext}"
            table_out.rename(columns={t2_ext: tout_ext}, inplace=True)
            table_out[tout_ext] = table2[t2_ext] - table1[t1_ext]
            # subtract our values
            table_out["yadism"] -= table1["yadism"]
            table_out["yadism_error"] += table1["yadism_error"]

            # compute relative error
            def rel_err(row, tout_ext=tout_ext):
                if row[tout_ext] == 0.0:
                    if row["yadism"] == 0.0:
                        return 0.0
                    return np.nan
                else:
                    return (row["yadism"] / row[tout_ext] - 1.0) * 100

            table_out["percent_error"] = table_out.apply(rel_err, axis=1)

            # dump results' table
            diffout.print(obs, "-" * len(obs), sep="\n")
            diffout[obs] = table_out

        return diffout

    def check_log(self, doc_hash, perc_thr=1, abs_thr=1e-6):
        """
        Check if the log passed the default assertions

        Paramters
        ---------
            doc_hash : hash
                log hash
        """
        # TODO determine external, improve output
        dfd = self.log_as_dfd(doc_hash)
        for n, df in dfd.items():
            for l in df.iloc:
                if (
                    abs(l["percent_error"]) > perc_thr
                    and abs(l["APFEL"] - l["yadism"]) > abs_thr
                ):
                    print(n, l, sep="\n", end="\n\n")

    def crashed_log(self, doc_hash):
        """
        Check if the log passed the default assertions

        Paramters
        ---------
            doc_hash : hash
                log hash

        Returns
        -------
            cdfd : dict
                log without kinematics
        """
        dfd = self.log_as_dfd(doc_hash)
        if "_crash" not in dfd:
            raise ValueError("log didn't crash!")
        cdfd = {}
        for sf in dfd:
            if on.ObservableName.is_valid(sf):
                cdfd[sf] = f"{len(dfd[sf])} points"
            else:
                cdfd[sf] = dfd[sf]
        return cdfd

    # def join(self, id1, id2):
    #     tabs = []
    #     tabs1 = []
    #     exts = []
    #     suffixes = (f" ({id1})", f" ({id2})")

    #     for i, doc_hash in enumerate([id1, id2]):
    #         tabs += [self.get_log_DFdict(doc_hash)[0]]
    #         tabs1 += [tabs[i].drop(["yadism", "yadism_error", "percent_error"], axis=1)]
    #         exts += [
    #             tabs1[i].columns.drop(["x", "Q2"])[0]
    #         ]  # + suffixes[i]] # to do: the suffixes are not working as expected

    #     def rel_err(row):
    #         ref = row[exts[0]]
    #         cmp = row[exts[1]]
    #         if ref != 0:
    #             return (cmp / ref - 1) * 100
    #         else:
    #             return np.nan

    #     tab_joint = tabs1[0].merge(
    #         tabs1[1], on=["x", "Q2"], how="outer", suffixes=suffixes
    #     )
    #     tab_joint["ext_rel_err [%]"] = tab_joint.apply(rel_err, axis=1)

    #     if all(np.isclose(tabs[0]["yadism"], tabs[1]["yadism"])):
    #         tab_joint["yadism"] = tabs[0]["yadism"]
    #         tab_joint["yadism_error"] = tabs[0]["yadism_error"]
    #     else:
    #         pass

    #     return tab_joint
