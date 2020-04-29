#!/usr/bin/env python3
from pprint import pprint
import pathlib

import pandas as pd
from tinydb import TinyDB, Query

# database access
here = pathlib.Path(__file__).parent.absolute()
idb = TinyDB(here / "data" / "input.json")

# Theory ------------------
# all theories

def get_all_theories():
    # collect
    return idb.table("theories").all()

def list_all_theories():
    # collect
    theories = get_all_theories()
    data = []
    for t in theories:
        obj = {"doc_id": t.doc_id}
        for f in ["PTO","XIF","XIR","PDFSet"]:
            obj[f] = t[f]
        data.append(obj)
    # output
    df = pd.DataFrame(data)
    return df

def print_all_theories():
    l = list_all_theories()
    print(l)

# one theory
def get_theory(doc_id):
    return idb.table("theories").get(doc_id=doc_id)

def pprint_theory(doc_id):
    t = get_theory(doc_id)
    pprint(t,sort_dicts=False)

# Observables -------------------
# all
def get_all_observables():
    # collect
    return idb.table("observables").all()

def list_all_observables():
    # collect
    obs = get_all_observables()
    data = []
    for o in obs:
        obj = {"doc_id": o.doc_id}
        xgrid = o["xgrid"]
        obj["xgrid"] = "[{}, ..., {}] ({}) ".format(min(xgrid),max(xgrid),len(xgrid))
        obj["log"] = o["is_log_interpolation"]
        obj["degree"] = o["polynomial_degree"]
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
    l = list_all_observables()
    print(l)

# one observable
def get_observable(doc_id):
    return idb.table("observables").get(doc_id=doc_id)

def pprint_observable(doc_id):
    t = get_observable(doc_id)
    pprint(t,sort_dicts=False)

# common
def collect(table):
    if table == "theories":
        return list_all_theories()
    elif table == "observables":
        return list_all_observables()
    else:
        print(f"Unkown table: {table}")
        return []

def p(table, doc_id = None):
    # list all
    if doc_id is None:
        if table == "theories":
            return print_all_theories()
        elif table == "observables":
            return print_all_observables()
        else:
            print(f"Unkown table: {table}")
    else: # list one
        if table == "theory":
            return pprint_theory(doc_id)
        elif table == "observable":
            return pprint_observable(doc_id)
        else:
            print(f"Unkown table: {table}")
    return None
