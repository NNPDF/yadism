# -*- coding: utf-8 -*-
import pathlib
from datetime import datetime
import argparse

import numpy as np

from .. import mode_selector
from ..utils import str_datetime

here = pathlib.Path(__file__).parent.absolute()


class ObservablesGenerator(mode_selector.ModeSelector):
    """
        Compile all theories to compare against

        Parameters
        ----------
            mode : str
                active mode
    """

    def __init__(self, mode):
        super(ObservablesGenerator, self).__init__(mode)
        self.observables_table = None

    def get_observables(self):
        # default interpolation setup
        interpolation_xgrid = np.unique(
            np.concatenate(
                [np.logspace(-4, np.log10(0.15), 20), np.linspace(0.15, 1.0, 12)]
            )
        )
        interpolation_polynomial_degree = 4
        interpolation_is_log = True
        content = dict(
            interpolation_xgrid=interpolation_xgrid.tolist(),
            interpolation_polynomial_degree=interpolation_polynomial_degree,
            interpolation_is_log=interpolation_is_log,
            prDIS="EM",
        )
        # use only a small set in regression
        if self.mode == "regression":
            content["F2light"] = [dict(x=0.01, Q2=90), dict(x=0.8, Q2=190)]
            content["FLlight"] = [dict(x=0.1, Q2=190)]
            for kind in ["F2", "FL"]:
                content[f"{kind}charm"] = [dict(x=0.01, Q2=50)]
                content[f"{kind}bottom"] = [dict(x=0.01, Q2=100)]
                content[f"{kind}top"] = [dict(x=0.01, Q2=1000)]
                content[f"{kind}total"] = [dict(x=0.01, Q2=90)]
            return content
        return content

    def write_observables(self, observables):
        """Insert all test options"""
        for obs in observables:
            obs["_modify_time"] = str_datetime(datetime.now())
            self.observables_table.insert(obs)

    def fill(self):
        """Fill table in DB"""
        # check intention
        if self.mode != "sandbox":
            ask = input(f"Do you want to refill the {self.mode} theories? [y/n]")
            if ask != "y":
                print("Nothing done.")
                return
        # load db
        print(f"writing to {self.input_name}")
        self.observables_table = self.idb.table("observables")
        # clear and refill
        self.observables_table.truncate()
        self.write_observables(self.get_observables())


def run_parser():
    # setup
    ap = argparse.ArgumentParser()
    arggroup = ap.add_mutually_exclusive_group()
    arggroup.add_argument(
        "--mode",
        choices=["APFEL", "QCDNUM", "regression", "sandbox"],
        default="sandbox",
        help="input DB to fill",
    )
    # do it
    args = ap.parse_args()
    tg = ObservablesGenerator(args.mode)
    tg.fill()
