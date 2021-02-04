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
        self.run(
            [{"PTO": 1}],
            observables.build(**(observables.default_config[1])),
            ["ToyLH"],
        )


@pytest.mark.skip
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
    def theory_updates(pto):
        # There is a QCDNUM error: "STOP ZMSTFUN: You cant vary both Q2 and muR2 scales --> STOP"
        # this is a limitation of QCDNUM in principle, so you have to work around it, i.e. fix Q2 and only
        # vary muR or vice versa
        sv = {"XIR": [0.5, 2.0], "XIF": [0.5, 1.0, 2.0], "PTO": [pto]}
        # XIR = 0.5 and XIF = 2.0 or viceversa are forbidden
        return filter(lambda c: (c["XIR"] * c["XIF"] != 1.0), power_set(sv))

    def benchmark_lo(self):
        self.run(
            self.theory_updates(0), self.observable_updates(), ["ToyLH"],
        )

    def benchmark_nlo(self):

        self.run(
            self.theory_updates(1), self.observable_updates(), ["ToyLH"],
        )


@pytest.mark.skip
class BenchmarkFNS(QCDNUMBenchmark):

    """Vary Flavor Number Schemes"""

    @staticmethod
    def observable_updates(fnames, q2s=None):

        if q2s == None:
            q2min = 4.0
            q2max = 1000.0
            q2fix = 20
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
            # {"NfFF": 3, "fnames": ["F2charm", "FLcharm",], "Q2range": [4,16]},
            # {"NfFF": 4, "fnames": ["F2bottom", "FLbottom",], "Q2range": [22, 40]},
            {"NfFF": 5, "fnames": ["F2top", "FLtop",], "Q2range": [90, 1000]},
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
    # p = pathlib.Path(__file__).parents[1] / "data" / "benchmark.db"
    # p.unlink(missing_ok=True)

    # plain = BenchmarkPlain()
    # plain.benchmark_lo()
    # plain.benchmark_nlo()

    sv = BenchmarkScaleVariations()
    # sv.benchmark_nlo()

    # TODO: check ZM and Ftop
    # TODO: mix fns ans sv
    fns = BenchmarkFNS()
    fns.benchmark_ZM()
    fns.benchmark_FFNS()


# class QCDNUMBenchmark:
#     """Wrapper to apply some default settings"""

#     db = None

#     def _db(self, assert_external=None):
#         """init DB connection"""
#         self.db = DBInterface("QCDNUM", assert_external=assert_external)
#         return self.db

#     def run_external(
#         self, PTO, pdfs, theory_update=None, obs_query=None, assert_external=None
#     ):
#         """Query for PTO also in obs by default"""
#         self._db(assert_external)
#         if obs_query is None:
#             obs_query = self.db.obs_query.PTO == PTO
#             if (
#                 PTO > 0
#             ):  # by default we're running in FFNS3, so we can use the big runcard
#                 obs_query &= self.db.obs_query.F2charm.exists()
#         return self.db.run_external(
#             PTO,
#             pdfs,
#             theory_update,
#             obs_query,
#         )


# @pytest.mark.quick_check
# @pytest.mark.commit_check
# class BenchmarkPlain(QCDNUMBenchmark):
#     """The most basic checks"""

#     def benchmark_LO(self):
#         return self.run_external(0, ["ToyLH"])

#     def benchmark_NLO(self):
#         return self.run_external(1, ["ToyLH"])


# class BenchmarkScaleVariations(QCDNUMBenchmark):
#     """Vary factorization and renormalization scale"""

#     def benchmark_LO(self):
#         return self.run_external(
#             0, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
#         )

#     def benchmark_NLO(self):
#         return self.run_external(
#             1, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
#         )


# class BenchmarkFNS(QCDNUMBenchmark):
#     """Flavor Number Schemes"""

#     def benchmark_LO(self):
#         return self.run_external(
#             0,
#             ["CT14llo_NF6"],
#             {"FNS": ~(self._db().theory_query.FNS == "FONLL-A"), "NfFF": None},
#         )

#     def _benchmark_NLO_FFNS3(self):
#         self._db()
#         return self.db.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {
#                 "FNS": self.db.theory_query.FNS == "FFNS",
#                 "NfFF": self.db.theory_query.NfFF == 3,
#             },
#             (self.db.obs_query.PTO == 1) & (self.db.obs_query.F2charm.exists()),
#         )

#     def _benchmark_NLO_FFNS4(self):
#         self._db()
#         return self.db.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {
#                 "FNS": self.db.theory_query.FNS == "FFNS",
#                 "NfFF": self.db.theory_query.NfFF == 4,
#             },
#             (self.db.obs_query.PTO == 1)
#             & (self.db.obs_query.F2bottom.exists())
#             & (~(self.db.obs_query.F2charm.exists())),
#         )

#     def _benchmark_NLO_FFNS5(self):
#         self._db()
#         return self.db.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {
#                 "FNS": self.db.theory_query.FNS == "FFNS",
#                 "NfFF": self.db.theory_query.NfFF == 5,
#             },
#             (self.db.obs_query.PTO == 1)
#             & (self.db.obs_query.F2top.exists())
#             & (~(self.db.obs_query.F2bottom.exists())),
#         )

#     def _benchmark_NLO_ZM_VFNS(self):
#         self._db()
#         return self.db.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {"FNS": self.db.theory_query.FNS == "ZM-VFNS"},
#             (self.db.obs_query.PTO == 1)
#             & (self.db.obs_query.F2light.exists())
#             & (~(self.db.obs_query.F2charm.exists())),
#         )

#     def benchmark_NLO(self):
#         self._benchmark_NLO_FFNS3()
#         self._benchmark_NLO_FFNS4()
#         self._benchmark_NLO_FFNS5()
#         self._benchmark_NLO_ZM_VFNS()


# if __name__ == "__main__":
#     # plain = BenchmarkPlain()
#     # plain.benchmark_LO()
#     # plain.benchmark_NLO()

#     # fns = BenchmarkFNS()
#     # fns._benchmark_NLO_FFNS5()

#     sc = BenchmarkScaleVariations()
#     sc.benchmark_NLO()
