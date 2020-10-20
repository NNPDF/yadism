# -*- coding: utf-8 -*-
from datetime import datetime
import argparse
import pathlib
import copy

import numpy as np
import yaml
import rich.progress

from .. import mode_selector
from ..utils import str_datetime
from . import power_set

here = pathlib.Path(__file__).parent


class TheoriesGenerator(mode_selector.ModeSelector):
    """
        Compile all theories to compare against

        Parameters
        ----------
            mode : str
                active mode
    """

    def get_matrix(self):
        """Gather all available options"""
        # QCDNUM has only limited options
        if self.mode == "QCDNUM":
            return {
                "PTO": [0, 1],
                "XIR": [0.5, 1.0, 2.0],
                "XIF": [0.5, 1.0, 2.0],
                "NfFF": [3, 4, 5],
                "FNS": ["FFNS", "ZM-VFNS"],
            }
        # we're aiming for a APFEL replacement, so they appread naturally together
        if self.mode in ["APFEL", "regression"]:
            return {
                "PTO": [0, 1],
                "XIR": [0.5, 0.7, 1.0, 2.0],
                "XIF": [0.5, 0.7, 1.0, 2.0],
                "TMC": [0, 1],
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
            "FNS": ["FFNS", "ZM-VFNS", "FONLL-A", "FONLL-A'"],
            "DAMP": [0, 1],
        }

    def write_matrix(self, matrix):
        """Insert all test options"""
        # read template
        with open(here / "theory_template.yaml") as f:
            template = yaml.safe_load(f)
        # get all possible combinations
        theories_table = self.idb.table("theories")
        theories_table.truncate()
        full = power_set(matrix)
        theories = []
        for config in rich.progress.track(
            full, total=np.prod([len(v) for v in matrix.values()])
        ):
            template.update(config)
            template["_modify_time"] = str_datetime(datetime.now())
            theories.append(copy.copy(template))
        # write
        print(f"writing {len(theories)} cards to {self.input_name}")
        theories_table.insert_multiple(theories)

    def fill(self):
        """Fill table in DB"""
        # check intention
        if self.mode != "sandbox":
            ask = input(f"Do you want to refill the {self.mode} theories? [y/n]")
            if ask != "y":
                print("Nothing done.")
                return
        # load db
        matrix = self.get_matrix()
        # clear and refill
        self.write_matrix(matrix)


def run_parser():
    # setup
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        choices=["APFEL", "QCDNUM", "regression", "sandbox"],
        default="sandbox",
        help="input DB to fill",
    )
    # do it
    args = ap.parse_args()
    tg = TheoriesGenerator(args.mode)
    tg.fill()
