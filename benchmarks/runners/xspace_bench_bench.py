# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

# import pytest
# from yadmark.benchmark.db_interface import DBInterface, QueryFieldsEqual

import pathlib
import copy
import pytest
import numpy as np

from banana.data import power_set

from yadmark.benchmark.runner import Runner
from yadmark.data import observables


class xspaceBenchmark(Runner):
    """
    Globally set the external program to xspace_bench
    """

    external = "xspace_bench"


class BenchmarkPlain(xspaceBenchmark):

    """The most basic checks"""

    def benchmark_lo(self):
        self.run([{}], observables.build(**(observables.default_config[0])), ["ToyLH"])

    def benchmark_nlo(self):
        self.run(
            [{"PTO": 1}],
            observables.build(**(observables.default_config[1])),
            ["ToyLH"],
        )


@pytest.mark.skip
class BenchmarkFNS(xspaceBenchmark):

    """Vary Flavor Number Schemes"""

    @staticmethod
    def observable_updates(FX):

        obs_cards = []
        for proc in FX.keys():
            kinematics = []
            kinematics.extend(
                [dict(x=x, Q2=10.0) for x in np.geomspace(0.0001, 0.90, 10).tolist()]
            )
            kinematics.extend(
                [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4.0, 16.0, 10).tolist()]
            )
            observable_names = FX[proc]
            obs_card = dict(
                observable_names=observable_names,
                kinematics=kinematics,
                update={"prDIS": [proc]},
            )
            obs_cards.extend(observables.build(**(obs_card)))

        return obs_cards

    def benchmark_ZM(self):

        fnames = [
            "F2total",
            "FLtotal",
        ]
        FX = {
            "CC": fnames + ["F3total"],
            "NC": fnames,
        }
        fns = {"NfFF": [3, 4, 5], "FNS": ["ZM-VFNS"], "PTO": [1]}

        self.run(power_set(fns), self.observable_updates(FX), ["ToyLHAPDF"])

    def benchmark_FFNS(self):

        fnames = [
            "F2light",
            "F2total",
            "F2charm",
            "FLlight",
            "FLtotal",
            "FLcharm",
        ]
        FX = {
            "CC": fnames + ["F3charm", "F3total"],
            "NC": fnames,
        }
        fns = {"NfFF": [3], "FNS": ["FFNS"], "PTO": [1]}

        self.run(power_set(fns), self.observable_updates(FX), ["ToyLHAPDF"])

    def benchmark_FONLL(self):

        fnames = [
            "F2light",
            "F2total",
            "F2charm",
            "FLlight",
            "FLtotal",
            "FLcharm",
        ]
        FX = {
            "CC": fnames + ["F3charm", "F3total"],
            "NC": fnames,
        }
        fns = {"NfFF": [4], "FNS": ["FONLL-A"], "PTO": [1]}
        self.run(power_set(fns), self.observable_updates(FX), ["ToyLHAPDF"])


if __name__ == "__main__":

    # plain = BenchmarkPlain()
    # plain.benchmark_lo()
    # plain.benchmark_nlo()

    fns = BenchmarkFNS()
    fns.benchmark_ZM()
    fns.benchmark_FFNS()
    fns.benchmark_FONLL()
