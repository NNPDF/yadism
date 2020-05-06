#!/usr/bin/env python3
from pprint import pprint
import pathlib
from datetime import datetime
import sys

import numpy as np
import pandas as pd
from tinydb import TinyDB, Query

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / "aux"))
from apfel_utils import unstr_datetime  # pylint:disable=import-error

# database access
here = pathlib.Path(__file__).parent.absolute()
idb = TinyDB(here / "data" / "input.json")
odb = TinyDB(here / "data" / "output.json")

# Theory ------------------
# all theories


def get_all_theories():
    """Retrieve all theories from db."""
    # collect
    return idb.table("theories").all()


def list_all_theories():
    """Collect important information of all theories."""
    # collect
    theories = get_all_theories()
    data = []
    for t in theories:
        obj = {"doc_id": t.doc_id}
        for f in ["PTO", "XIF", "XIR", "TMC"]:
            obj[f] = t[f]
        dt = unstr_datetime(t["_modify_time"])
        obj["modified"] = pretty_date(dt)
        data.append(obj)
    # output
    df = pd.DataFrame(data)
    return df


def print_all_theories():
    """Print overview of theories."""
    l = list_all_theories()
    print(l)


# one theory
def get_theory(doc_id):
    """
        Retrieve an theory.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    return idb.table("theories").get(doc_id=doc_id)


def pprint_theory(doc_id):
    """
        Pretty print a theory.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    t = get_theory(doc_id)
    pprint(t, sort_dicts=False)


def purge_theories():
    """Purge theories table."""
    ask = input("Purge theories table? [y/n]")
    if ask == "y":
        idb.table("theories").purge()
    else:
        print("nothing done.")


# Observables -------------------
# all
def get_all_observables():
    """Retrieve all observables from db."""
    # collect
    return idb.table("observables").all()


def list_all_observables():
    """Collect important information of all observables."""
    # collect
    obs = get_all_observables()
    data = []
    for o in obs:
        obj = {"doc_id": o.doc_id}
        xgrid = o["xgrid"]
        obj["xgrid"] = "[{}, ..., {}] ({}) ".format(min(xgrid), max(xgrid), len(xgrid))
        obj["log"] = o["is_log_interpolation"]
        obj["degree"] = o["polynomial_degree"]
        dt = unstr_datetime(o["_modify_time"])
        obj["modified"] = pretty_date(dt)
        sfs = []
        esfs = 0
        for sf in o:
            # quick fix
            if sf[0] != "F":
                continue
            sfs.append(sf)
            esfs += len(o[sf])
        obj["structure_functions"] = " ".join(sfs) + f" at {esfs} points"
        data.append(obj)
    # output
    df = pd.DataFrame(data)
    return df


def print_all_observables():
    """Print overview of observables."""
    l = list_all_observables()
    print(l)


# one observable
def get_observable(doc_id):
    """
        Retrieve an observable.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    return idb.table("observables").get(doc_id=doc_id)


def pprint_observable(doc_id):
    """
        Pretty print an observable.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    t = get_observable(doc_id)
    pprint(t, sort_dicts=False)


def purge_observables():
    """Purge observables table."""
    ask = input("Purge observables table? [y/n]")
    if ask == "y":
        idb.table("observables").purge()
    else:
        print("nothing done.")


# Logs -------------------
# all
def get_all_logs():
    """Retrieve all logs from db."""
    # collect
    return odb.table("logs").all()


# TODO replace with Alessandro's version
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"


def list_all_logs():
    """Collect important information of all logs."""
    # collect
    logs = get_all_logs()
    data = []
    for l in logs:
        obj = {"doc_id": l.doc_id}
        sfs = []
        esfs = 0
        for sf in l:
            # quick fix
            if sf[0] != "F":
                continue
            sfs.append(sf)
            esfs += len(l[sf])
        obj["structure_functions"] = " ".join(sfs) + f" at {esfs} points"
        for f in ["_theory_doc_id", "_observables_doc_id", "_creation_time", "_pdf"]:
            obj[f.split("_")[1]] = l[f]
        dt = unstr_datetime(obj["creation"])
        obj["creation"] = pretty_date(dt)
        data.append(obj)
    # output
    df = pd.DataFrame(data)
    return df


def print_all_logs():
    """Print overview of log."""
    l = list_all_logs()
    print(l)


# one observable
def get_log(doc_id):
    """
        Retrieve a log.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    return odb.table("logs").get(doc_id=doc_id)


def pprint_log(doc_id):
    """
        Pretty print a log.

        Parameters
        ----------
            doc_id : int
                document identifier
    """
    t = get_log(doc_id)
    pprint(t, sort_dicts=False)


def purge_logs():
    """Purge logs table."""
    ask = input("Purge logs table? [y/n]")
    if ask == "y":
        odb.table("logs").purge()
    else:
        print("nothing done.")


# detectors
t = "t"


def _is_theory(table, plural=True):
    """wrapper to activate theory"""
    if table == t:
        return True
    if plural:
        return table == "theories"
    return table == "theory"


o = "o"


def _is_obs(table, plural=True):
    """wrapper to activate observables"""
    if table == o:
        return True
    if plural:
        return table == "observables"
    return table == "observable"


l = "l"


def _is_log(table, plural=True):
    """wrapper to activate logs"""
    if table == l:
        return True
    if plural:
        return table == "logs"
    return table == "log"


# common
def ls(table):
    """
        List wrapper.

        Parameters
        ----------
            table : str
                table name to query: short cut or plural
    """
    if _is_theory(table):
        return list_all_theories()
    elif _is_obs(table):
        return list_all_observables()
    elif _is_log(table):
        return list_all_logs()
    else:
        print(f"Unkown table: {table}")
        return []


def p(table, doc_id=None):
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
        if _is_theory(table):
            print_all_theories()
        elif _is_obs(table):
            print_all_observables()
        elif _is_log(table):
            print_all_logs()
        else:
            print(f"Unkown table: {table}")
    else:  # list one
        if _is_theory(table, False):
            pprint_theory(doc_id)
        elif _is_obs(table, False):
            pprint_observable(doc_id)
        elif _is_log(table, False):
            pprint_log(doc_id)
        else:
            print(f"Unkown table: {table}")


def g(table, doc_id=None):
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
        if _is_theory(table):
            r = get_all_theories()
        elif _is_obs(table):
            r = get_all_observables()
        elif _is_log(table):
            r = get_all_logs()
        else:
            print(f"Unkown table: {table}")
    else:  # list one
        if _is_theory(table, False):
            r = get_theory(doc_id)
        elif _is_obs(table, False):
            r = get_observable(doc_id)
        elif _is_log(table, False):
            r = get_log(doc_id)
        else:
            print(f"Unkown table: {table}")
    return r


get = g


def subtract_tables(id1, id2):
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

        TODO:
            output the table: since there are many table produced by this
            function output instead a suitable object
            the object should be iterable so you can explore all the values,
            but it has a __str__ (or __repr__?) method that will automatically
            loop and print if its dropped directly in the interpreter
    """

    class DiffOut(list):
        def __repr__(self):
            for i in self:
                print(i)
            return None

    # print head
    msg = f"Subtracting id:{id1} - id:{id2}, in table 'logs'"
    print(msg, "=" * len(msg), sep="\n")
    print()

    # load json documents
    log1 = get_log(id1)
    log2 = get_log(id2)
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


diff = subtract_tables


def yelp(*args):
    """
        Help function (renamed to avoid clash of names) - short cut: h.
    """
    if len(args) == 0:
        print(
            f"""Welcome to yadism benchmark skript!
Available short cuts (variables):
    t = "{t}" -> "theor[y|ies]"
    o = "{o}" -> "observable[s]"
    l = "{l}" -> "log[s]"
Available functions (selected list):
    g - getter
    ls - listing (reduced information)
    p - printing (using ls)
    diff - subtractig logs"""
        )
    elif len(args) == 1:
        return help(*args)
    return None


h = yelp


# TODO: to be adjusted
def compare_dicts(d1, d2):
    for x, y in zip(d1.items(), d2.items()):
        if x[1] != y[1]:
            print(x[0], y[0])
