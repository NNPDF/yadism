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
    def observable_updates():

        # TODO: add FXlight FXcharm when available (not in ZM-VFNS)
        obs_cards = []
        updates = [
            {"prDIS": ["CC"]},
            {"prDIS": ["NC"]},
        ]

        for update in updates:
            kinematics = []
            kinematics.extend(
                [dict(x=x, Q2=10.0) for x in np.geomspace(0.0001, 0.99, 10).tolist()]
            )
            kinematics.extend(
                [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4.0, 16.0, 10).tolist()]
            )
            observable_names = [
                "F2total",
                "FLtotal",
                "F3total",
            ]
            obs_card = dict(
                observable_names=observable_names, kinematics=kinematics, update=update
            )
            obs_cards.extend(observables.build(**(obs_card)))

        return obs_cards

    @staticmethod
    def theory_updates(pto):

        fns = {"NfFF": [3, 4, 5], "FNS": ["ZM-VFNS", "FFNS", "FONLL-A"], "PTO": [pto]}
        return filter(
            lambda c: not (
                (c["NfFF"] != 4.0 and c["FNS"] == "FONLL-A")
                or (c["NfFF"] != 3.0 and c["FNS"] == "FFNS")
            ),
            power_set(fns),
        )

    def benchmark_nlo(self):

        self.run(
            self.theory_updates(1), self.observable_updates(), ["ToyLHAPDF"],
        )


if __name__ == "__main__":

    # plain = BenchmarkPlain()
    # plain.benchmark_lo()
    # plain.benchmark_nlo()

    fns = BenchmarkFNS()
    fns.benchmark_nlo()
