from pprint import pprint

import numpy as np
import pandas as pd
from tinydb import TinyDB
from human_dates import human_dates

from yadism import observable_name as on

from ..utils import unstr_datetime
from .. import mode_selector
from .df_list import DFlist
from . import table_manager as tm

t = "t"
o = "o"
l = "l"


class NavigatorApp(mode_selector.ModeSelector):
    def __init__(self, mode):
        super(NavigatorApp, self).__init__(mode)
        self.theories = tm.TableManager(self.idb.table("theories"))
        self.observable = tm.TableManager(self.idb.table("observable"))
        self.apfel_cache = tm.TableManager(self.idb.table("apfel_cache"))
        self.qcdnum_cache = tm.TableManager(self.idb.table("qcdnum_cache"))
        self.logs = tm.TableManager(self.odb.table("logs"))

    def change_mode(self, mode):
        """Change mode"""
        super(NavigatorApp, self).__init__(mode)

    def get_all_theories(self):
        """Retrieve all theories from db."""
        # collect
        return self.idb.table("theories").all()

    def get(self, table, doc_id=None):
        """
        Getter wrapper.

        Parameters
        ----------
            table : str
                table name to query: short cut or singular for one document or plural for all
            doc_id :
                if given, retrieve single document
        """
        r = None
        # list all
        if doc_id is None:
            if self._is_theory(table):
                r = self.get_all_theories()
            elif self._is_obs(table):
                r = self.get_all_observables()
            elif self._is_log(table):
                r = self.get_all_logs()
            else:
                print(f"Unkown table: {table}")
        else:  # list one
            if self._is_theory(table, False):
                r = self.get_theory(doc_id)
            elif self._is_obs(table, False):
                r = self.get_observable(doc_id)
            elif self._is_log(table, False):
                r = self.get_log(doc_id)
            else:
                print(f"Unkown table: {table}")
        return r

    def list_all_theories(self):
        """Collect important information of all theories."""
        # collect
        theories = self.get_all_theories()
        data = []
        for t in theories:
            obj = {"doc_id": t.doc_id}
            for f in ["PTO", "XIF", "XIR", "TMC", "NfFF", "FNS"]:
                obj[f] = t[f]
            dt = unstr_datetime(t["_modify_time"])
            obj["modified"] = human_dates(dt)
            data.append(obj)
        # output
        df = pd.DataFrame(data)
        return df

    def print_all_theories(self):
        """Print overview of theories."""
        l = self.list_all_theories()
        print(l)

    # one theory
    def get_theory(self, doc_id):
        """
            Retrieve an theory.

            Parameters
            ----------
                doc_id : int
                    document identifier
        """
        return self.idb.table("theories").get(doc_id=doc_id)

    def pprint_theory(self, doc_id):
        """
            Pretty print a theory.

            Parameters
            ----------
                doc_id : int
                    document identifier
        """
        t = self.get_theory(doc_id)
        pprint(t, sort_dicts=False)

    def get_all_observables(self):
        """Retrieve all observables from db."""
        return self.idb.table("observables").all()

    def list_all_observables(self):
        """Collect important information of all observables."""
        # collect
        obs = self.get_all_observables()
        data = []
        for o in obs:
            obj = {"doc_id": o.doc_id}
            if "PTO" in o:
                obj["PTO"] = o["PTO"]
            xgrid = o["interpolation_xgrid"]
            obj[
                "xgrid"
            ] = f"{len(xgrid)}pts: {'log' if o['interpolation_is_log'] else 'x'}^{o['interpolation_polynomial_degree']}"
            obj["curr"] = o["prDIS"]
            proj_map = {
                "electron": "e-",
                "positron": "e+",
                "neutrino": "ν",
                "antineutrino": "ν~",
            }
            obj["proj"] = proj_map[o["projectile"]]
            obj["pol"] = o["PolarizationDIS"]
            sfs = 0
            esfs = 0
            for sf in o:
                # quick fix
                if not on.ObservableName.is_valid(sf):
                    continue
                sfs += 1
                esfs += len(o[sf])
            obj["structure_functions"] = f"{sfs} SF @ {esfs} points"
            dt = unstr_datetime(o["_modify_time"])
            obj["modified"] = human_dates(dt)
            data.append(obj)
        # output
        df = pd.DataFrame(data)
        return df

    def print_all_observables(self):
        """Print overview of observables."""
        l = self.list_all_observables()
        print(l)

    # one observable
    def get_observable(self, doc_id):
        """
            Retrieve an observable.

            Parameters
            ----------
                doc_id : int
                    document identifier
        """
        return self.idb.table("observables").get(doc_id=doc_id)

    def pprint_observable(self, doc_id):
        """
            Pretty print an observable.

            Parameters
            ----------
                doc_id : int
                    document identifier
        """
        t = self.get_observable(doc_id)
        pprint(t, sort_dicts=False)

    def get_all_logs(self):
        """Retrieve all logs from db."""
        # collect
        return self.odb.table("logs").all()

    def list_all_logs(self):
        """Collect important information of all logs."""
        # collect
        logs = self.get_all_logs()
        data = []
        for l in logs:
            obj = {"doc_id": l.doc_id}
            sfs = 0
            esfs = 0
            for sf in l:
                if not on.ObservableName.is_valid(sf):
                    continue
                sfs += 1
                esfs += len(l[sf])
            crash = l.get("_crash", None)
            if crash is None:
                obj["structure_functions"] =  f"{sfs} SF @ {esfs} pts"
            else:
                obj[
                    "structure_functions"
                ] = f"{crash} for {l['_crash_sf']} at {l['_crash_kin']}"
            for f in [
                "_theory_doc_id",
                "_observables_doc_id",
                "_creation_time",
                "_pdf",
            ]:
                if f in l.keys():
                    obj[f.split("_")[1]] = l[f]
            dt = unstr_datetime(obj["creation"])
            obj["creation"] = human_dates(dt)
            data.append(obj)
        # output
        df = pd.DataFrame(data)
        return df

    def print_all_logs(self):
        """Print overview of log."""
        l = self.list_all_logs()
        print(l)

    # one observable
    def get_log(self, doc_id):
        """
            Retrieve a log.

            Parameters
            ----------
                doc_id : int
                    document identifier

            Returns
            -------
                log : dict
                    document
        """
        return self.odb.table("logs").get(doc_id=doc_id)

    def truncate_logs(self):
        """Truncate all logs"""
        if input("Purge all logs? [y/n]") != "y":
            print("Doing nothing.")
            return
        return self.odb.table("logs").truncate()

    def get_log_DataFrames(self, doc_id):
        """
            Load all structure functions in log as DataFrame

            Parameters
            ----------
                doc_id : int
                    document identifier

            Returns
            -------
                log : list(pd.DataFrame)
                    DataFrames
        """
        l = self.get_log(doc_id)
        dfs = DFlist()
        for k in l:
            # TODO
            if k[0] != "F":
                continue
            dfs.print(f"{k} with theory={l['_theory_doc_id']} using {l['_pdf']}")
            dfs.register(pd.DataFrame(l[k]))
        return dfs

    def pprint_log(self, doc_id):
        """
            Pretty print a log.

            Parameters
            ----------
                doc_id : int
                    document identifier
        """
        t = self.get_log(doc_id)
        pprint(t, sort_dicts=False)

    def _is_theory(self, table, plural=True):
        """wrapper to activate theory"""
        if table == t:
            return True
        if plural:
            return table == "theories"
        return table == "theory"

    def _is_obs(self, table, plural=True):
        """wrapper to activate observables"""
        if table == o:
            return True
        if plural:
            return table == "observables"
        return table == "observable"

    def _is_log(self, table, plural=True):
        """wrapper to activate logs"""
        if table == l:
            return True
        if plural:
            return table == "logs"
        return table == "log"

    def list_all(self, table):
        """
            List wrapper.

            Parameters
            ----------
                table : str
                    table name to query: short cut or plural
        """
        print(self._is_theory(table))
        if self._is_theory(table):
            return self.list_all_theories()
        elif self._is_obs(table):
            return self.list_all_observables()
        elif self._is_log(table):
            return self.list_all_logs()
        else:
            print(f"Unkown table: {table}")
            return []

    def print(self, table, doc_id=None):
        """
            Print wrapper.

            Parameters
            ----------
                table : str
                    table name to query: short cut or singular for one document or plural for list
                doc_id :
                    if given, print single document
        """
        # list all
        if doc_id is None:
            if self._is_theory(table):
                self.print_all_theories()
            elif self._is_obs(table):
                self.print_all_observables()
            elif self._is_log(table):
                self.print_all_logs()
            else:
                print(f"Unkown table: {table}")
        else:  # list one
            if self._is_theory(table, False):
                self.pprint_theory(doc_id)
            elif self._is_obs(table, False):
                self.pprint_observable(doc_id)
            elif self._is_log(table, False):
                self.pprint_log(doc_id)
            else:
                print(f"Unkown table: {table}")

    def subtract_tables(self, id1, id2):
        """
            Subtract results in the second table from the first one,
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

        diffout = DFlist()

        # print head
        msg = f"Subtracting id:{id1} - id:{id2}, in table 'logs'"
        diffout.print(msg, "=" * len(msg), sep="\n")
        diffout.print()

        # load json documents
        log1 = self.get_log(id1)
        log2 = self.get_log(id2)
        if log1 is None:
            raise ValueError(f"Log id:{id1} not found")
        if log2 is None:
            raise ValueError(f"Log id:{id2} not found")

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
            known_col_set = set(["x", "Q2", "yadism", "yadism_error", "rel_err[%]"])
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
            def rel_err(row):
                if row[tout_ext] == 0.0:
                    if row["yadism"] == 0.0:
                        return 0.0
                    return np.nan
                else:
                    return (row["yadism"] / row[tout_ext] - 1.0) * 100

            table_out["rel_err[%]"] = table_out.apply(rel_err, axis=1)

            # dump results' table
            diffout.print(obs, "-" * len(obs), sep="\n")
            diffout.register(table_out)

        return diffout

    def join(self, id1, id2):
        tabs = []
        tabs1 = []
        exts = []
        suffixes = (f" ({id1})", f" ({id2})")

        for i, doc_id in enumerate([id1, id2]):
            tabs += [self.get_log_DataFrames(doc_id)[0]]
            tabs1 += [tabs[i].drop(["yadism", "yadism_error", "rel_err[%]"], axis=1)]
            exts += [
                tabs1[i].columns.drop(["x", "Q2"])[0]
            ]  # + suffixes[i]] # TODO the suffixes are not working as expected

        def rel_err(row):
            ref = row[exts[0]]
            cmp = row[exts[1]]
            if ref != 0:
                return (cmp / ref - 1) * 100
            else:
                return np.nan

        tab_joint = tabs1[0].merge(
            tabs1[1], on=["x", "Q2"], how="outer", suffixes=suffixes
        )
        tab_joint["ext_rel_err [%]"] = tab_joint.apply(rel_err, axis=1)

        if all(np.isclose(tabs[0]["yadism"], tabs[1]["yadism"])):
            tab_joint["yadism"] = tabs[0]["yadism"]
            tab_joint["yadism_error"] = tabs[0]["yadism_error"]
        else:
            pass

        return tab_joint

    def compare_dicts(self, d1, d2, exclude_underscored=False):
        """
            Check which entries of the two dictionaries are different, and output
            the values.
        """
        kw = 20  # keys print width
        fw = 30  # values print width0
        print("┌", "─" * (kw + 2), "┬", "─" * (fw * 2 + 1 + 2), "┐", sep="")
        for k in d1.keys() | d2.keys():
            if exclude_underscored and k[0] == "_":
                continue

            if k not in d1:
                print(f"│ {k:<{kw}} │ {None:>{fw}} {d2[k]:>{fw}} │")
            elif k not in d2:
                print(f"│ {k:<{kw}} │ {d1[k]:>{fw}} {None:>{fw}} │")
            elif d1[k] != d2[k]:
                print(f"│ {k:<{kw}} │ {d1[k]:>{fw}} {d2[k]:>{fw}} │")
        print("└", "─" * (kw + 2), "┴", "─" * (fw * 2 + 1 + 2), "┘", sep="")
