# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's
import pathlib

import pytest

from banana.data import power_set

from yadmark.benchmark.runner import Runner
from yadmark.data import observables


class ApfelBenchmark(Runner):
    """
    Globally set the external program to APFEL
    """

    external = "APFEL"


class BenchmarkPlain(ApfelBenchmark):
    def benchmark_lo(self):
        self.run(
            [{}], observables.build(**(observables.default_config[0])), ["CT14llo_NF3"]
        )

    def benchmark_nlo(self):
        self.run(
            [{"PTO": 1}],
            observables.build(**(observables.default_config[1])),
            ["ToyLH"],
        )


@pytest.mark.skip  # commit_check
class BenchmarkProjectile(ApfelBenchmark):
    """The most basic checks"""

    update = {
        "prDIS": ["NC", "CC"],
        "ProjectileDIS": ["electron", "positron", "neutrino", "antineutrino"],
        "PolarizationDIS": [0.0, -0.6, 1.0],
    }  # amounts to 2*4*3 = 24 cards

    def benchmark_lo(self):
        obs_update = observables.build(
            **(observables.default_config[0]), update=self.update
        )
        self.run([{"PTO": 0}], obs_update, ["ToyLH"])

    def benchmark_nlo(self):
        obs_update = observables.build(
            **(observables.default_config[1]), update=self.update
        )
        self.run([{"PTO": 1}], obs_update, ["ToyLH"])


# def tmc_assert_external(theory, _obs, sf, yad):
#     # turning point (maybe again a cancelation of channels?)
#     if sf in ["F2light", "F2total"] and yad["x"] > 0.9:
#         return dict(abs=1e-4)
#     # same as in plain
#     if sf == "FLbottom" and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2:
#         # APFEL has a discreization in Q2/m2
#         return dict(abs=1e-5)
#     # FL TMC is broken in APFEL
#     # https://github.com/scarrazza/apfel/issues/23
#     if sf[:2] == "FL" and yad["x"] > 0.3:
#         return dict(abs=1e-2)
#     return None


@pytest.mark.skip  # commit_check
class BenchmarkTMC(ApfelBenchmark):
    """Add Target Mass Corrections"""

    def benchmark_lo(self):
        cfg = observables.default_config[0].copy()
        # turning point (maybe again a cancelation of channels?)
        # or maybe the interpolation is just breaking down
        cfg["kinematics"] = list(filter(lambda k: k["x"] < 0.9, cfg["kinematics"]))
        obs_updates = observables.build(**cfg, update={"prDIS": "CC"})
        self.run([{"PTO": 0, "TMC": 1}], obs_updates, ["ToyLH"])

    def benchmark_nlo(self):
        cfg = observables.default_config[1].copy()
        cfg["kinematics"] = list(filter(lambda k: k["x"] < 0.9, cfg["kinematics"]))
        obs_updates = observables.build(**cfg, update={"prDIS": "CC"})
        # FL TMC is broken in APFEL
        # https://github.com/scarrazza/apfel/issues/23
        small_kins = list(
            filter(lambda k: k["x"] < 0.2 and k["Q2"] > 4.5, cfg["kinematics"])
        )
        obs_updates[0]["observables"].update(
            {"FLlight": small_kins, "FLcharm": small_kins}
        )
        self.run([{"PTO": 1, "TMC": 1}], obs_updates, ["ToyLH"])


@pytest.mark.skip
class BenchmarkScaleVariations(ApfelBenchmark):

    # TODO add observable generator
    # the observables eventually need to be taylored to the used theories,
    # i.e. configuration need to be more scattered in this this class.
    # The physical reason is that, for XIR beeing small pQCD becomes unreliable
    # and thus we can NOT probe as low Q2 as before.

    @staticmethod
    def theory_updates(pto):
        # TODO include FNS variations
        # again we might scatter this more among in this class
        sv = {"XIR": [0.5, 1.0, 2.0], "XIF": [0.5, 1.0, 2.0], "PTO": [pto]}
        # drop plain
        return filter(
            lambda c: not (c["XIR"] == 1.0 and c["XIF"] == 1.0), power_set(sv)
        )

    def benchmark_lo(self):
        self.run(
            self.theory_updates(0),
            observables.build(**(observables.default_config[0])),
            ["ToyLH"],
        )

    def benchmark_nlo(self):
        self.run(
            self.theory_updates(1),
            observables.build(**(observables.default_config[1])),
            ["ToyLH"],
        )


if __name__ == "__main__":
    p = pathlib.Path(__file__).absolute().parents[1] / "data" / "benchmark.db"
    # p.unlink(missing_ok=True)

    plain = BenchmarkPlain()
    # plain.benchmark_lo()
    # plain.benchmark_nlo()

    proj = BenchmarkTMC()
    proj.benchmark_nlo()

# def plain_assert_external(theory, obs, sf, yad):
#     # APFEL has a discretization in Q2/m2
#     if sf == "FLcharm" and yad["Q2"] < 1.5 * theory["mc"] ** 2:
#         return dict(abs=3e-5)
#     if sf == "FLbottom" and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2:
#         return dict(abs=5e-6)
#     if obs["prDIS"] == "CC":
#         if sf[2:] == "charm" and yad["x"] > 0.75:
#             return dict(abs=2e-6)  # grid border
#         if sf[2:] == "top" and yad["Q2"] < 150:
#             return dict(abs=1e-4)  # production threshold
#         if sf == "F3total":
#             # we have a change in sign (from + to - at small Q2 and back to + at large)
#             # F3light is > 0, but F3charm < 0
#             return dict(rel=0.03)
#     return None


# def sv_assert_external(theory, obs, sf, yad):
#     if np.isclose(theory["XIF"], 1) and np.isclose(theory["XIR"], 1):
#         return plain_assert_external(theory, obs, sf, yad)
#     if sf == "FLbottom" and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2:
#         # APFEL has a discreization in Q2/m2
#         return dict(abs=1e-5)
#     if sf == "FLcharm" and yad["Q2"] < 7:
#         return dict(rel=0.015)
#     if obs["prDIS"] == "CC":
#         if sf[2:] == "top":
#             if yad["Q2"] < 160:
#                 return dict(abs=2e-4)  # production threshold
#             if sf[:2] == "F3" and yad["Q2"] > 900:
#                 return dict(abs=3e-5)  # why does the thing go worse again?
#         if sf == "F3charm" and yad["x"] < 2e-3:
#             # there is a cancelation between sbar and g going on:
#             # each of the channels is O(1) with O(1e-3) accuracy
#             return dict(abs=5e-3)
#         if sf == "F3total":
#             # still F3light is > 0, but F3charm < 0
#             return dict(rel=0.1)
#     if theory["XIF"] < 1 or theory["XIR"] < 1:
#         # for small xir pQCD becomes unreliable
#         if sf in ["F2light", "F2total"] and yad["Q2"] < 7:
#             return dict(abs=5e-2)
#     return None


# @pytest.mark.commit_check
# class BenchmarkScaleVariations(ApfelBenchmark):
#     """Vary factorization and renormalization scale"""

#     def benchmark_LO(self):
#         return self.run_external(
#             0, ["CT14llo_NF3"], {"XIR": None, "XIF": None}, {"prDIS": None}
#         )

#     def benchmark_NLO(self):
#         return self.run_external(
#             1,
#             ["CT14llo_NF3"],
#             {
#                 "XIR": None,
#                 "XIF": None,
#             },
#             {"prDIS": None},
#             assert_external=sv_assert_external,
#         )


# class BenchmarkFNS(ApfelBenchmark):
#     """Flavor Number Schemes"""

#     def benchmark_LO(self):
#         return self.run_external(
#             0,
#             ["CT14llo_NF6"],
#             {"FNS": ~(self._db().theory_query.FNS.search("FONLL-")), "NfFF": None},
#         )

#     def benchmark_NLO_FFNS(self):
#         def ffns_assert(theory, obs, sf, yad):
#             if theory["NfFF"] < 5:
#                 return plain_assert_external(theory, obs, sf, yad)
#             # TODO https://github.com/N3PDF/yadism/wiki/2020_05_28-F2charm-FFNS4-low-Q2-non-zero
#             if (
#                 theory["NfFF"] == 5
#                 and sf[2:] in ["bottom", "total"]
#                 and yad["Q2"] < theory["mb"] ** 2
#             ):
#                 return False
#             return None

#         return self.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {
#                 "FNS": self._db().theory_query.FNS == "FFNS",
#                 "NfFF": self._db().theory_query.NfFF != 3,
#             },
#             assert_external=ffns_assert,
#         )

#     def benchmark_NLO_ZM_VFNS(self):
#         return self.run_external(
#             1, ["CT14llo_NF6"], {"FNS": self._db().theory_query.FNS == "ZM-VFNS"}
#         )

#     @pytest.mark.skip
#     @pytest.mark.fonll
#     def benchmark_NLO_FONLL(self):
#         def fonll_assert(theory, _obs, sf, yad):
#             if (
#                 sf == "FLbottom"
#                 and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2
#             ):
#                 # APFEL has a discreization in Q2/m2
#                 return dict(abs=5e-6)
#             if sf == "FLcharm" and yad["Q2"] < 7 and theory["DAMP"] == 1:
#                 return dict(abs=2e-5)
#             return None

#         return self.run_external(
#             1,
#             ["CT14llo_NF6"],
#             {"FNS": self._db().theory_query.FNS == "FONLL-A", "DAMP": None},
#             assert_external=fonll_assert,
#         )
