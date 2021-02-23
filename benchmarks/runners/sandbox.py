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
    #external = "xspace_bench"
    #external = "QCDNUM"
    #external = "void"

    alphas_from_lhapdf = True

    @staticmethod
    def generate_observables():
        defaults = copy.deepcopy(observables.default_card)
        # xgrid = np.array(defaults["interpolation_xgrid"]).copy()
        #interpolation_xgrid = np.linspace(1e-1, 1, 9).tolist()
        interpolation_xgrid = list(reversed([1,
            0.9309440808717544,
            0.8627839323906108,
            0.7956242522922756,
            0.7295868442414312,
            0.6648139482473823,
            0.601472197967335,
            0.5397572337880445,
            0.4798989029610255,
            0.4221667753589648,
            0.3668753186482242,
            0.31438740076927585,
            0.2651137041582823,
            0.2195041265003886,
            0.17802566042569432,
            0.14112080644440345,
            0.10914375746330703,
            0.08228122126204893,
            0.060480028754447364,
            0.04341491741702269,
            0.030521584007828916,
            0.02108918668378717,
            0.014375068581090129,
            0.009699159574043398,
            0.006496206194633799,
            0.004328500638820811,
            0.0028738675812817515,
            0.0019034634022867384,
            0.0012586797144272762,
            0.0008314068836488144,
            0.0005487795323670796,
            0.00036205449638139736,
            0.00023878782918561914,
            0.00015745605600841445,
            0.00010381172986576898,
            6.843744918967896e-05,
            4.511438394964044e-05,
            2.97384953722449e-05,
            1.9602505002391748e-05,
            1.292101569074731e-05,
            8.516806677573355e-06,
            5.613757716930151e-06,
            3.7002272069854957e-06,
            2.438943292891682e-06,
            1.607585498470808e-06,
            1.0596094959101024e-06,
            6.984208530700364e-07,
            4.6035014748963906e-07,
            3.034304765867952e-07,
            1.9999999999999954e-07]))

        kinematics = []
        kinematics.extend(
            #[dict(x=0.1,Q2=90)]
            [dict(x=x, Q2=50.0) for x in interpolation_xgrid[::3]]
            #[dict(x=x, Q2=90.0) for x in np.linspace(1e-1, 1, 5)]
        )
        # kinematics.extend([dict(x=x, Q2=90) for x in np.linspace(.8, .99, 10).tolist()])
        kinematics.extend([dict(x=0.10914375746330703, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        # kinematics.extend([dict(x=0.0051, Q2=Q2) for Q2 in np.geomspace(10, 1e5, 60).tolist()])
        # kinematics = [dict(x=0.001,Q2=1e4)]
        # kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(500, 800, 10).tolist()])
        # kinematics.extend([dict(x=0.1, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        observable_names = [
            "F2light",
            # "F2charm",
            # "F2bottom",
            # "F2top",
            # "F2total",
            # "FLlight",
            # "FLcharm",
            # "FLbottom",
            # "FLtotal",
            # "F3light",
            # "F3charm",
            # "F3bottom",
            # "F3total",
        ]
        update = {"prDIS": ["EM"],"interpolation_xgrid":[interpolation_xgrid], "interpolation_polynomial_degree": [4]}
        #update={"interpolation_xgrid":[defaults["interpolation_xgrid"]], "interpolation_polynomial_degree": [defaults["interpolation_polynomial_degree"]]}
        # card["interpolation_xgrid"] = list(card["interpolation_xgrid"])
        # card["interpolation_xgrid"] = list(reversed(pineappl_zgrid))
        # card["interpolation_is_log"] = False
        # card["PropagatorCorrection"] = .999
        # card["ProjectileDIS"] = "antineutrino"
        # card["PolarizationDIS"] = 0.5
        return dict(observable_names=observable_names,kinematics=kinematics,update=update)

    def doit(self):
        self.run([{"PTO": 0}],
                observables.build(**(self.generate_observables())), ["CT14llo_NF3"])


if __name__ == "__main__":
    sand = Sandbox()
    sand.doit()
