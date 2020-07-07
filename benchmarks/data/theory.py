import pathlib
import itertools
import sys
from datetime import datetime
import argparse

import yaml
import tinydb

# import numpy as np
here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from external_utils import (  # pylint:disable=import-error,wrong-import-position
    str_datetime,
)

def my_product(inp):
    """
    Thank you: https://stackoverflow.com/questions/5228158/
    """
    return [
        dict(zip(inp.keys(), values)) for values in itertools.product(*inp.values())
    ]

class TheoriesGenerator:
    """
        Compile all theories to compare against
    """
    def __init__(self, mode):
        self.mode = mode
        self.theories_table = None

    def get_matrix(self):
        """Gather all available options"""
        if self.mode == "QCDNUM":
            return {
                "PTO": [0, 1],
                "XIR": [0.5, 1.0, 2.0],
                "XIF": [0.5, 1.0, 2.0],
                "NfFF": [3, 4, 5],
                "FNS": ["FFNS", "ZM-VFNS"],
            }
        # we're aiming for a APFEL replacement, so they appread naturally together
        if self.mode == "APFEL" or self.mode == "regression":
            return {
                "PTO": [0, 1],
                "XIR": [0.5, 1.0, 2.0],
                "XIF": [0.5, 1.0, 2.0],
                "TMC": [0, 1, 2, 3],
                "NfFF": [3, 4, 5],
                "FNS": ["FFNS", "ZM-VFNS", "FONLL-A"],
                "DAMP": [0, 1],
            }
        # sandbox
        return {
            "PTO": [0, 1],
            "XIR": [0.5, 1.0, 2.0],
            "XIF": [0.5, 1.0, 2.0],
            "TMC": [0, 1, 2, 3],
            "NfFF": [3, 4, 5],
            "FNS": ["FFNS", "ZM-VFNS", "FONLL-A"],
            "DAMP": [0, 1],
        }

    def get_db_name(self):
        """Determine DB name"""
        if self.mode == "regression":
            return "regression.json"
        if self.mode == "APFEL":
            return "apfel-input.json"
        if self.mode == "QCDNUM":
            return "qcdnum-input.json"
        # sandbox
        return "input.json"

    def write_matrix(self, matrix):
        """Insert all test options"""
        # read template
        with open(here / "theory_template.yaml") as f:
            template = yaml.safe_load(f)
        # write all possible combinations
        for config in my_product(matrix):
            template.update(config)
            template["_modify_time"] = str_datetime(datetime.now())
            self.theories_table.insert(template)

    def fill(self):
        """Fill table in DB"""
        # check intention
        if self.mode != "sandbox":
            ask = input(f"Do you want to refill the {self.mode} theories? [y/n]")
            if ask != "y":
                print("Nothing done.")
                return
        # lod db
        db_name = self.get_db_name()
        print(f"writing to {db_name}")
        db = tinydb.TinyDB(here / db_name)
        self.theories_table = db.table("theories")
        # clear and refill
        self.theories_table.truncate()
        self.write_matrix(self.get_matrix())

if __name__ == "__main__":
    # setup
    ap = argparse.ArgumentParser()
    arggroup = ap.add_mutually_exclusive_group()
    arggroup.add_argument("--mode", choices=["APFEL", "QCDNUM", "regression", "sandbox"], default="sandbox", help="input DB to fill")
    # do it
    args = ap.parse_args()
    tg = TheoriesGenerator(args.mode)
    tg.fill()
