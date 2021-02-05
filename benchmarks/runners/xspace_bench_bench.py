# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

import numpy as np

from banana.data import power_set

from yadmark.benchmark.runner import Runner
from yadmark.data import observables


class XspaceBenchmark(Runner):
    """
    Globally set the external program to xspace_bench
    """

    external = "xspace_bench"


class BenchmarkPlain(XspaceBenchmark):
    """The most basic checks"""

    def benchmark_lo(self):
        self.run([{}], observables.build(**(observables.default_config[0])), ["ToyLHAPDF"])

    def benchmark_nlo(self):
        self.run(
            [{"PTO": 1}],
            observables.build(**(observables.default_config[1])),
            ["ToyLHAPDF"],
        )


class BenchmarkFNS(XspaceBenchmark):
    """Vary Flavor Number Schemes"""

    @staticmethod
    def observable_updates(FX, q2_min=None, q2_max=None):

        # Bench mark only in physical ranges
        if q2_min is None:
            q2_min = 4.0
        if q2_max is None:
            q2_max = 16.0

        obs_cards = []
        for proc in FX.keys():
            kinematics = []
            kinematics.extend(
                [dict(x=x, Q2=10.0) for x in np.geomspace(0.0001, 0.75, 10).tolist()]
            )
            kinematics.extend(
                [
                    dict(x=0.001, Q2=Q2)
                    for Q2 in np.geomspace(q2_min, q2_max, 10).tolist()
                ]
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

        fnames = ["F2total", "FLtotal", "F3total"]
        FX = {
            "CC": fnames,
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
            "F3light",
        ]
        FX = {
            "CC": fnames + ["F3charm"],
            "NC": fnames,
        }
        fns = {"NfFF": [3], "FNS": ["FFNS"], "PTO": [1]}

        self.run(power_set(fns), self.observable_updates(FX), ["ToyLHAPDF"])

        # F3total should be computed separatly due to cancellations in quark contributions
        FX = {"CC": ["F3total"]}
        # with gonly
        self.run(power_set(fns), self.observable_updates(FX), ["toygonly"])
        # excluding the low q2 region.
        q2 = 6
        self.run(power_set(fns), self.observable_updates(FX, q2_min=q2), ["ToyLHAPDF"])

    def benchmark_FONLL(self):

        fnames = [
            "F2light",
            "F2total",
            "F2charm",
            "FLlight",
            "FLtotal",
            "FLcharm",
            "F3light",
        ]
        FX = {
            "CC": fnames + ["F3charm"],
            "NC": fnames,
        }
        fns = {"NfFF": [4], "FNS": ["FONLL-A"], "PTO": [1], "DAMP": [0, 1]}
        self.run(power_set(fns), self.observable_updates(FX), ["ToyLHAPDF"])

        # F3total should be computed separatly due to cancellations in quark contributions
        # (massive part)
        FX = {"CC": ["F3total"]}
        # with gonly
        self.run(power_set(fns), self.observable_updates(FX), ["toygonly"])
        # excluding the low q2 region.
        q2 = 6
        self.run(power_set(fns), self.observable_updates(FX, q2_min=q2), ["ToyLHAPDF"])


if __name__ == "__main__":

    plain = BenchmarkPlain()
    plain.benchmark_lo()
    # plain.benchmark_nlo()

    fns = BenchmarkFNS()
    fns.benchmark_ZM()
    #fns.benchmark_FFNS()
    #fns.benchmark_FONLL()
