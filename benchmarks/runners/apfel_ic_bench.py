# -*- coding: utf-8 -*-
#
# Compare the results for IC with APFEL's
import numpy as np

from yadmark.benchmark.runner import Runner


class ApfelICBenchmark(Runner):
    """
    Globally set the external program to APFEL
    """

    external = "APFEL"

    def obs_updates(self, allow_cc=False):
        kinematics = []
        kinematics.extend([dict(x=x, Q2=10.0) for x in np.geomspace(1e-5, 1, 10)])
        kinematics.extend(
            [dict(x=0.1, Q2=Q2) for Q2 in np.geomspace(4, 20, 10).tolist()]
        )
        obs = [
            {
                "prDIS": "NC",
                "observables": {f: kinematics for f in ["F2charm", "FLcharm"]},
            },
        ]
        obs.append(
            {
                "prDIS": "CC",
                "observables": {
                    f: kinematics for f in ["F2charm", "FLcharm", "F3charm"]
                },
            }
        )
        return obs


class BenchmarkFFNS(ApfelICBenchmark):
    def benchmark_lo(self):
        self.run([{"IC": 1}], self.obs_updates(True), ["conly", "CT14llo_NF4"])

    def benchmark_nlo(self):
        self.run([{"PTO": 1, "IC": 1}], self.obs_updates(), ["conly", "CT14llo_NF4"])


class BenchmarkFONLL(ApfelICBenchmark):
    def benchmark_nlo(self):
        self.run(
            [{"PTO": 1, "IC": 1, "FNS": "FONLL-A", "NfFF": 4}],
            self.obs_updates(),
            ["conly", "CT14llo_NF4"],
        )


if __name__ == "__main__":
    ffns = BenchmarkFFNS()
    ffns.benchmark_lo()
    ffns.benchmark_nlo()
    fonll = BenchmarkFONLL()
    fonll.benchmark_nlo()
