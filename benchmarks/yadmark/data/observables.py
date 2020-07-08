# -*- coding: utf-8 -*-
from datetime import datetime
import argparse
import copy

import numpy as np

from .. import mode_selector
from ..utils import str_datetime


class ObservablesGenerator(mode_selector.ModeSelector):
    """
        Compile all theories to compare against

        Parameters
        ----------
            mode : str
                active mode
    """

    def get_observables(self):
        """
            Collect all runcards

            Returns
            -------
                observables : list(dict)
                    list of runcards
        """
        # default interpolation setup
        interpolation_xgrid = np.unique(
            np.concatenate([np.geomspace(1e-4, 0.15, 20), np.linspace(0.15, 1.0, 12)])
        )
        interpolation_polynomial_degree = 4
        interpolation_is_log = True
        defaults = dict(
            interpolation_xgrid=interpolation_xgrid.tolist(),
            interpolation_polynomial_degree=interpolation_polynomial_degree,
            interpolation_is_log=interpolation_is_log,
            prDIS="EM",
        )
        # use only a small set in regression
        if self.mode == "regression":
            reg = copy.deepcopy(defaults)
            reg["F2light"] = [dict(x=0.01, Q2=90), dict(x=0.8, Q2=190)]
            reg["FLlight"] = [dict(x=0.1, Q2=190)]
            for kind in ["F2", "FL"]:
                reg[f"{kind}charm"] = [dict(x=0.01, Q2=50)]
                reg[f"{kind}bottom"] = [dict(x=0.01, Q2=100)]
                reg[f"{kind}top"] = [dict(x=0.01, Q2=1000)]
                reg[f"{kind}total"] = [dict(x=0.01, Q2=90)]
            return [reg]  # only use a single card
        if self.mode in ["APFEL", "QCDNUM"]:
            # fixed Q2 and fixed x
            light_kin = []
            light_kin.extend(
                [dict(x=x, Q2=90.0) for x in interpolation_xgrid[3::3].tolist()]
            )
            light_kin.extend(
                [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()]
            )
            # LO runcard - only F2light is non-zero
            lo_card = copy.deepcopy(defaults)
            lo_card["PTO"] = 0
            lo_card["F2light"] = copy.copy(light_kin)
            # NLO runcard
            nlo_card = copy.deepcopy(defaults)
            nlo_card["PTO"] = 1
            obs_list = [
                "F2light",
                "F2charm",
                "F2bottom",
                "F2top",
                "FLlight",
                "FLcharm",
                "FLbottom",
                "FLtop",
            ]
            # in APFEL total is accessible
            if self.mode == "APFEL":
                obs_list.extend(["F2total", "FLtotal"])
            for obs in obs_list:
                nlo_card[obs] = copy.copy(light_kin)  # for now take same kinematics
            return [lo_card, nlo_card]
        # sandbox
        sandbox = copy.deepcopy(defaults)
        return [sandbox]

    def write_observables(self, observables):
        """Insert all observables"""
        observables_table = self.idb.table("observables")
        observables_table.truncate()
        for obs in observables:
            obs["_modify_time"] = str_datetime(datetime.now())
            observables_table.insert(obs)

    def fill(self):
        """Fill table in DB"""
        # check intention
        if self.mode != "sandbox":
            ask = input(f"Do you want to refill the {self.mode} observables? [y/n]")
            if ask != "y":
                print("Nothing done.")
                return
        # load db
        print(f"writing to {self.input_name}")
        # clear and refill
        self.write_observables(self.get_observables())


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
    og = ObservablesGenerator(args.mode)
    og.fill()
