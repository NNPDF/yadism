# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

# import pytest
import numpy as np

from banana.data import power_set

from yadmark.benchmark.runner import Runner
from yadmark.data import observables


class QCDNUMBenchmark(Runner):
    """
    Globally set the external program to QCDNUM
    """

    external = "QCDNUM"


class BenchmarkPlain(QCDNUMBenchmark):
    """The most basic checks"""

    def benchmark_lo(self):
        self.run([{}], observables.build(**(observables.default_config[0])), ["ToyLH"])

    def benchmark_nlo(self):

        fnames =  {"observable_names": ["F2light", "FLlight", "F3light"],}
        obs =  observables.default_config[1].copy()
        obs.update(fnames)
        
        self.run(
            [{"PTO": 1}],
            observables.build(**(obs)),
            ["ToyLH"],
        )


# @pytest.mark.skip
class BenchmarkScaleVariations(QCDNUMBenchmark):
    """Vary factorization and renormalization scale"""

    @staticmethod
    def observable_updates():

        kinematics = []
        kinematics.extend(
            [dict(x=x, Q2=90.0) for x in np.geomspace(0.0001, 0.75, 10).tolist()]
        )
        kinematics.extend(
            [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4.0, 1000.0, 10).tolist()]
        )
        observable_names = [
            "F2light",
            "FLlight",
            "F3light",
        ]
        obs_card = dict(
            observable_names=observable_names,
            kinematics=kinematics,
            update={"prDIS": ["NC"]},
        )

        return observables.build(**(obs_card))

    @staticmethod
    def theory_updates(pto, FNS):
        # There is a QCDNUM error: "STOP ZMSTFUN: You cant vary both Q2 and muR2 scales --> STOP"
        # this is a limitation of QCDNUM in principle, so you have to work around it, i.e. fix Q2
        # and only vary muR or vice versa

        if FNS == 1:
            sv = {
                "XIR": [0.5, 2.0],
                "XIF": [0.5, 1.0, 2.0],
                "PTO": [pto],
                "NfFF": [3, 4, 5],
                "FNS": ["FFNS", "ZM-VFNS"],
            }
        else:
            sv = {
                "XIR": [0.5, 2.0],
                "XIF": [0.5, 1.0, 2.0],
                "PTO": [pto],
            }

        # XIR = 0.5 and XIF = 2.0 or viceversa are forbidden
        return filter(lambda c: (c["XIR"] * c["XIF"] != 1.0), power_set(sv))

    def benchmark_lo(self, FNS=0):
        self.run(
            self.theory_updates(0, FNS), self.observable_updates(), ["ToyLH"],
        )

    def benchmark_nlo(self, FNS=0):

        self.run(
            self.theory_updates(1, FNS), self.observable_updates(), ["ToyLH"],
        )


# @pytest.mark.skip
class BenchmarkFNS(QCDNUMBenchmark):
    """Vary Flavor Number Schemes"""

    @staticmethod
    def observable_updates(fnames, q2s=None):

        if q2s is None:
            q2min = 4.0
            q2max = 1000.0
            # note: due to the qgrid setting q2fix should be different from a mass threshold
            q2fix = 22
        else:
            q2min = q2s[0]
            q2max = q2s[1]
            q2fix = 0.5 * sum(q2s)

        kinematics = []
        kinematics.extend(
            [dict(x=x, Q2=q2fix) for x in np.geomspace(0.0001, 0.75, 10).tolist()]
        )
        kinematics.extend(
            [dict(x=0.0001, Q2=Q2) for Q2 in np.geomspace(q2min, q2max, 10).tolist()]
        )
        observable_names = fnames

        obs_card = dict(
            observable_names=observable_names,
            kinematics=kinematics,
            update={"prDIS": ["NC"]},
        )

        return observables.build(**(obs_card))

    def benchmark_ZM(self):

        fnames = [
            "F2light",
            "FLlight",
            "F3light",
        ]
        fns = {"NfFF": [3, 4, 5], "FNS": ["ZM-VFNS"], "PTO": [1]}

        self.run(power_set(fns), self.observable_updates(fnames), ["ToyLH"])

    def benchmark_FFNS(self):

        light_fnames = [
            "F2light",
            "FLlight",
            "F3light",
        ]
        heavy_fnames = [
            {"NfFF": 3, "fnames": ["F2charm", "FLcharm",], "Q2range": [4, 16]},
            {"NfFF": 4, "fnames": ["F2bottom", "FLbottom",], "Q2range": [22, 40]},
            # FLtop is always really small < 10^-6, there are some numerical differences
            # {"NfFF": 5, "fnames": ["F2top", "FLtop",], "Q2range": [90, 1000]},
            {"NfFF": 5, "fnames": ["F2top",], "Q2range": [150, 1000]},
        ]

        # loop over NfFF
        for item in heavy_fnames:
            fns = {"NfFF": [item["NfFF"]], "FNS": ["FFNS"], "PTO": [1]}
            self.run(
                power_set(fns),
                self.observable_updates(light_fnames + item["fnames"], item["Q2range"]),
                ["ToyLH"],
            )


if __name__ == "__main__":
    plain = BenchmarkPlain()
    plain.benchmark_lo()
    plain.benchmark_nlo()

    # You can benchmark FNS and SV for FXlight with FNS = 1
    sv = BenchmarkScaleVariations()
    sv.benchmark_nlo(FNS=0)

    fns = BenchmarkFNS()
    fns.benchmark_ZM()
    fns.benchmark_FFNS()
