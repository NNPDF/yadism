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

        obs_cards = []
        updates = [
            {"prDIS": ["CC"]},
            {"prDIS": ["NC"]},
        ]

        for update in updates:
            kinematics = []
            kinematics.extend(
                [dict(x=x, Q2=90.0) for x in np.geomspace(0.0001, 0.99, 10).tolist()]
            )
            observable_names = [
                "F2total",
                "F2light",
                "FLtotal",
                "FLlight",
            ]
            obs_card = dict(
                observable_names=observable_names, kinematics=kinematics, update=update
            )
            obs_cards.extend(observables.build(**(obs_card)))

        return obs_cards

    @staticmethod
    def theory_updates(pto):
        # TODO there is still a QCDNUM error: "STOP ZMSTFUN: You cant vary both Q2 and muR2 scales --> STOP"
        # this is a limitation of QCDNUM in principle, so you have to work around it, i.e. fix Q2 and only
        # vary muR or vice versa
        # For the moment fix Q2.
        sv = {"XIR": [0.5, 1.0, 2.0], "XIF": [0.5, 1.0, 2.0], "PTO": [pto]}
        # drop plain
        return filter(
            lambda c: not (c["XIR"] == 1.0 and c["XIF"] == 1.0), power_set(sv)
        )

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
    def observable_updates():

        # TODO: add FXbottom and FXcharm when they are available
        obs_cards = []
        updates = [
            {"prDIS": ["CC"]},
            {"prDIS": ["NC"]},
        ]

        for update in updates:
            kinematics = []
            kinematics.extend(
                [dict(x=x, Q2=90.0) for x in np.geomspace(0.0001, 0.99, 10).tolist()]
            )
            kinematics.extend(
                [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4.0, 1000.0, 10).tolist()]
            )
            observable_names = [
                "F2total",
                "F2light",
                "FLtotal",
                "FLlight",
            ]
            obs_card = dict(
                observable_names=observable_names, kinematics=kinematics, update=update
            )
            obs_cards.extend(observables.build(**(obs_card)))

        return obs_cards

    @staticmethod
    def theory_updates(pto):

        fns = {"NfFF": [3, 4, 5], "FNS": ["FFNS", "ZM-VFNS"], "PTO": [pto]}
        return power_set(fns)

    def benchmark_nlo(self):
        self.run(
            self.theory_updates(1), self.observable_updates(), ["ToyLH"],
        )


if __name__ == "__main__":
    # p = pathlib.Path(__file__).parents[1] / "data" / "benchmark.db"
    # p.unlink(missing_ok=True)

    # plain = BenchmarkPlain()
    # plain.benchmark_lo()
    # plain.benchmark_nlo()

    sv = BenchmarkScaleVariations()
    # sv.benchmark_nlo()

    fns = BenchmarkFNS()
    fns.benchmark_nlo()


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
