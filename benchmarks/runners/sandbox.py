# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
# Our testing playground
import copy

import numpy as np

from banana.data import power_set

from yadmark.benchmark.runner import Runner
from yadmark.data import observables

class Sandbox(Runner):

    external = "APFEL" # external comparison program

    @staticmethod
    def generate_observables():
        defaults = copy.deepcopy(observables.default_card)
        # xgrid = np.array(defaults["interpolation_xgrid"]).copy()
        # defaults["interpolation_xgrid"] = np.geomspace(0.1, 1, 40).tolist()
        kinematics = []
        kinematics.extend(
            [dict(x=x, Q2=90.0) for x in defaults["interpolation_xgrid"][3::3]]
            #np.linspace(1e-3, 1, 50)
        )
        # kinematics.extend([dict(x=x, Q2=90) for x in np.linspace(.8, .99, 10).tolist()])
        kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        # kinematics.extend([dict(x=0.0051, Q2=Q2) for Q2 in np.geomspace(10, 1e5, 60).tolist()])
        # kinematics = [dict(x=0.001,Q2=1e4)]
        # kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(500, 800, 10).tolist()])
        # kinematics.extend([dict(x=0.1, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        observable_names = [
            "F2light",
            "F2charm",
            # "F2bottom",
            # "F2top",
            "F2total",
            "FLlight",
            "FLcharm",
            # "FLbottom",
            "FLtotal",
            "F3light",
            "F3charm",
            # "F3bottom",
            "F3total",
        ]
        update = {"prDIS": ["CC"]}
        # card["interpolation_xgrid"] = list(card["interpolation_xgrid"])
        # card["interpolation_xgrid"] = list(reversed(pineappl_zgrid))
        # card["interpolation_is_log"] = False
        # card["PropagatorCorrection"] = .999
        # card["ProjectileDIS"] = "antineutrino"
        # card["PolarizationDIS"] = 0.5
        return dict(observable_names=observable_names,kinematics=kinematics,update=update)

    def _run(self):
        self.run([{}], observables.build(**(self.generate_observables())), ["CT14nlo_NF4"])


if __name__ == "__main__":
    sand = Sandbox()
    sand._run()
