"""
Compare the results with APFEL++'s
"""
import pathlib

import numpy as np
import pytest
from banana import register
from banana.data import cartesian_product

from yadmark.benchmark.runner import Runner
from yadmark.data import observables

register(pathlib.Path(__file__).parents[1])


class ApfelpyBenchmark(Runner):
    """
    Globally set the external program to APFEL++
    """

    external = "APFEL++"


class BenchmarkPlain(ApfelpyBenchmark):
    def benchmark_pto(self, pto):
        self.run(
            [{"PTO": pto}],
            observables.build(**(observables.default_config[pto])),
            ["ToyLH"],
        )


@pytest.mark.skip
class BenchmarkZeroMass(ApfelpyBenchmark):

    @staticmethod
    def theory_updates_zm(pto):
        sv = {
            "XIR": [1.0],
            "XIF": [1.0],
            "PTO": [pto],
            "FNS": ["ZM-VFNS"],
        }
        return cartesian_product(sv)

    @staticmethod
    def obs_updates_zm():
        kins = []
        kins.extend(
            [
                dict(x=x, Q2=10.0)
                for x in observables.default_card["interpolation_xgrid"][10::3]
            ]
        )
        kins.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(3, 1e4, 10).tolist()])
        obs_updates = observables.build(
            ["F2_total", "F3_total", "FL_total"], kins, update={"prDIS": ["NC"]}
        )
        return obs_updates

    @staticmethod
    def obs_updates_pol():
        kins = []
        kins.extend(
            [
                dict(x=x, Q2=10.0)
                for x in observables.default_card["interpolation_xgrid"][10::3]
            ]
        )
        kins.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(3, 1e4, 10).tolist()])
        obs_updates = observables.build(
            ["g1_total", "g4_total", "gL_total"], kins, update={"prDIS": ["NC"]}
        )
        return obs_updates

    def benchmark_zm(self, pto):
        self.run(
            self.theory_updates_zm(pto),
            self.obs_updates_zm(),
            ["ToyLH"],
        )

    def benchmark_polarized(self, pto):
        self.run(
            self.theory_updates_zm(pto),
            self.obs_updates_pol(),
            ["ToyLH"],
        )


if __name__ == "__main__":


    obj = BenchmarkZeroMass()
    # obj.benchmark_polarized(0)
    obj.benchmark_zm(0)
