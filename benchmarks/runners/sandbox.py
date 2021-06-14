# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
# Our testing playground
import copy

import numpy as np

from banana.data import cartesian_product

from yadmark.benchmark.runner import Runner
from yadmark.data import observables

class Sandbox(Runner):

    # external comparison program
    external = "APFEL"
    #external = "xspace_bench"
    #external = "QCDNUM"
    #external = "void"

    # alphas_from_lhapdf = True

    @staticmethod
    def generate_observables():
        defaults = copy.deepcopy(observables.default_card)
        xgrid = np.array(defaults["interpolation_xgrid"]).copy()
        #interpolation_xgrid = np.linspace(1e-1, 1, 9).tolist()
        kinematics = []
        kinematics.extend(
            #[dict(x=0.1,Q2=90, y=0)]
            #[dict(x=x, Q2=20.0) for x in xgrid[:-1:5]]
            [dict(x=x, Q2=20.0, y=0) for x in np.geomspace(1e-4, .9, 10)]
        )
        kinematics.extend(
            [dict(x=x, Q2=1.51**2, y=0) for x in np.geomspace(1e-4, .9, 10)]
        )
        # kinematics.extend([dict(x=x, Q2=90) for x in np.linspace(.8, .99, 10).tolist()])
        #kinematics.extend([dict(x=0.10914375746330703, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        # kinematics.extend([dict(x=0.0051, Q2=Q2) for Q2 in np.geomspace(10, 1e5, 60).tolist()])
        # kinematics = [dict(x=0.001,Q2=1e4)]
        # kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(500, 800, 10).tolist()])
        kinematics.extend([dict(x=0.1, Q2=Q2,y=0) for Q2 in np.geomspace(4, 20, 10).tolist()])
        kinematics.extend([dict(x=0.001, Q2=Q2,y=0) for Q2 in np.geomspace(4, 20, 10).tolist()])
        observable_names = [
            "F2_light",
            #"F2_charm",
            # "F2_bottom",
            # "F2_top",
            #"F2_total",
            "FL_light",
            #"FL_charm",
            # "FL_bottom",
            # "FL_total",
            "F3_light",
            #"F3_charm",
            # "F3_bottom",
            # "F3_total",
            #  "XSHERANC",
            #"XSHERACC_light",
            #"XSHERACC_charm",
            #"XSCHORUSCC_light",
            #"XSCHORUSCC_charm",
            #"XSCHORUSCC",
            #"XSNUTEVCC_charm"
        ]
        #update = {"prDIS": ["EM"],"interpolation_xgrid":[interpolation_xgrid], "interpolation_polynomial_degree": [4]}
        update = {"prDIS": ["NC"], "ProjectileDIS": ["electron"]}
        #update = {"prDIS": ["EM"], "ProjectileDIS": ["electron"], "TargetDIS":["lead"]}
        #update= {}
        # card["PropagatorCorrection"] = .999
        # card["ProjectileDIS"] = "antineutrino"
        # card["PolarizationDIS"] = 0.5
        return observables.build(observable_names=observable_names,kinematics=kinematics,update=update)

    def doit(self):
        self.run([{"PTO": 2}], self.generate_observables(), ["Sonly"])

if __name__ == "__main__":
    sand = Sandbox()
    sand.doit()
