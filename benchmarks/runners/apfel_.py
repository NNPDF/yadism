"""
Compare the results with APFEL's


decoupled:
- [v] plain
- [v] projectile + polarization
- [v] propagator_correction
- [v] TMC
- [v] XS

combined:
- process + FNS(3) + SV
- process + IC + FNS(2) + SV
"""

import pathlib

import numpy as np
import pytest
from banana import register
from banana.data import cartesian_product

from yadmark.benchmark.runner import Runner
from yadmark.data import observables

register(pathlib.Path(__file__).parents[1])


class ApfelBenchmark(Runner):
    """
    Globally set the external program to APFEL
    """

    external = "APFEL"


class BenchmarkPlain(ApfelBenchmark):
    def benchmark_pto(self, pto):
        self.run(
            [{"PTO": pto}],
            observables.build(**(observables.default_config[pto])),
            ["ToyLH"],
        )


class BenchmarkProjectile(ApfelBenchmark):
    update = {
        "prDIS": ["NC", "CC"],
        "ProjectileDIS": ["electron", "positron", "neutrino", "antineutrino"],
        "PolarizationDIS": [0.0, -0.6, 1.0],
    }  # amounts to 2*4*3 = 24 cards

    def benchmark_pto(self, pto):
        obs_update = observables.build(
            **(observables.default_config[pto]), update=self.update
        )
        self.run([{"PTO": pto}], obs_update, ["ToyLH"])


class BenchmarkPositivity(ApfelBenchmark):
    update = {
        "NCPositivityCharge": ["up", "down", "strange", "all"],
    }

    def benchmark_pto(self, pto):
        obs_update = observables.build(
            **(observables.default_config[pto]), update=self.update
        )
        self.run([{"PTO": pto}], obs_update, ["ToyLH"])


class BenchmarkPropagatorCorrection(ApfelBenchmark):
    update = {
        "prDIS": ["NC", "CC"],
        "PropagatorCorrection": [1.0, 1e3],
    }  # amounts to 2*2 = 4 cards

    def benchmark_pto(self, pto):
        obs_update = observables.build(
            **(observables.default_config[pto]), update=self.update
        )
        self.run([{"PTO": pto}], obs_update, ["ToyLH"])


class BenchmarkTMC(ApfelBenchmark):
    """Check Target Mass Corrections"""

    def benchmark_lo(self):
        cfg = observables.default_config[0].copy()
        # turning point (maybe again a cancelation of channels?)
        # or maybe the interpolation is just breaking down
        cfg["kinematics"] = list(filter(lambda k: k["x"] < 0.9, cfg["kinematics"]))
        obs_updates = observables.build(**cfg, update={"prDIS": ["CC"]})
        self.run([{"PTO": 0, "TMC": 1}], obs_updates, ["ToyLH"])

    def benchmark_nlo(self):
        cfg = observables.default_config[1].copy()
        cfg["kinematics"] = list(filter(lambda k: k["x"] < 0.9, cfg["kinematics"]))
        obs_updates = observables.build(**cfg, update={"prDIS": ["CC"]})
        # FL TMC is broken in APFEL
        # https://github.com/scarrazza/apfel/issues/23
        small_kins = list(
            filter(lambda k: k["x"] < 0.2 and k["Q2"] > 4.5, cfg["kinematics"])
        )
        obs_updates[0]["observables"].update(
            {"FL_light": small_kins, "FL_charm": small_kins}
        )
        self.run([{"PTO": 1, "TMC": 1}], obs_updates, ["ToyLH"])


class BenchmarkXS(ApfelBenchmark):
    """Check cross sections"""

    def benchmark_pto(self, pto):
        kins = observables.default_kinematics.copy()
        obs_updates = observables.build(["XSHERANC"], kins, update={"prDIS": ["NC"]})
        obs_updates.extend(
            observables.build(["XSHERACC"], kins, update={"prDIS": ["CC"]})
        )
        obs_updates.extend(
            observables.build(
                ["XSCHORUSCC"],
                kins,
                update={
                    "prDIS": ["CC"],
                    "TargetDIS": ["isoscalar", "lead"],
                    "ProjectileDIS": ["neutrino"],
                },
            )
        )
        obs_updates.extend(
            observables.build(
                ["XSNUTEVCC_charm"],
                kins,
                update={
                    "prDIS": ["CC"],
                    "TargetDIS": ["iron"],
                    "ProjectileDIS": ["antineutrino"],
                },
            )
        )
        self.run([{"PTO": pto}], obs_updates, ["ToyLH"])

    # ============================================================================ #
    #                               ZM-VFNS                                        #
    # ============================================================================ #


@pytest.mark.skip
class BenchmarkFlavorNumberScheme(ApfelBenchmark):
    # TODO add observable generator
    # the observables eventually need to be taylored to the used theories,
    # i.e. configuration need to be more scattered in this this class.
    # The physical reason is that, for XIR beeing small pQCD becomes unreliable
    # and thus we can NOT probe as low Q2 as before.

    @staticmethod
    def theory_updates_zm(pto):
        sv = {
            # "XIR": [0.5, 2.0],
            # "XIF": [0.5, 2.0],
            "PTO": [pto],
            "FNS": ["ZM-VFNS"],
        }
        return cartesian_product(sv)

    @staticmethod
    def obs_updates_zm():
        kins = []
        # kins.extend(
        #     [
        #         dict(x=x, Q2=10.0)
        #         for x in observables.default_card["interpolation_xgrid"][3::3]
        #     ]
        # )
        kins.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(5, 1e4, 10).tolist()])
        obs_updates = observables.build(
            ["F2_total", "F3_total", "FL_total"], kins, update={"prDIS": ["NC", "CC"]}
        )
        return obs_updates

    def benchmark_zm(self, pto):
        self.run(
            self.theory_updates_zm(pto),
            self.obs_updates_zm(),
            ["ToyLH"],
        )

    # ============================================================================ #
    #                               FFNS                                           #
    # ============================================================================ #

    @staticmethod
    def theory_updates_ffns(pto):
        sv = {
            # "XIR": [0.5, 2.0],
            # "XIF": [0.5, 2.0],
            "PTO": [pto],
            "FNS": ["FFNS"],
            "mb": [1e7],
            "mt": [1e8],
            "NfFF": [3],
            "Qref": [1.9],
            "nfref": [3],
        }
        # theory_updates = cartesian_product(sv)
        # sv["NfFF"] = [5]
        # theory_updates.append(cartesian_product(sv))
        return cartesian_product(sv)

    @staticmethod
    def obs_updates_ffns():
        kins = []
        kins.extend(
            [
                dict(x=x, Q2=10.0)
                for x in observables.default_card["interpolation_xgrid"][12::3]
            ]
        )
        kins.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(10, 20, 5).tolist()])
        obs_updates = observables.build(
            [
                # "F2_total",
                # "F2_charm",
                # "F2_bottom",
                "F2_light"
            ],
            kins,
            update={
                "prDIS": [
                    "NC",
                    # "CC"
                ]
            },
        )
        return obs_updates

    def benchmark_ffns(self, pto):
        self.run(
            self.theory_updates_ffns(pto),
            self.obs_updates_ffns(),
            ["NNPDF40_nnlo_as_01180"],
        )

    # ============================================================================ #
    #                               FFN0                                           #
    # ============================================================================ #

    @staticmethod
    def theory_updates_ffn0(pto):
        sv = {
            # "XIR": [0.5, 2.0],
            # "XIF": [0.5, 2.0],
            # "kcThr": [np.inf],
            # "kbThr": [np.inf],
            # "ktThr": [np.inf],
            "PTO": [pto],
            "FNS": ["FFN0"],
            "mb": [1e7],
            "mt": [1e8],
            "NfFF": [3],
            "Qref": [1.9],
            "nfref": [3],
        }
        return cartesian_product(sv)

    @staticmethod
    def obs_updates_ffn0():
        kins = []
        kins.extend(
            [
                dict(x=x, Q2=10**2)
                for x in observables.default_card["interpolation_xgrid"][12::3]
            ]
        )
        kins.extend([dict(x=0.001, Q2=Q**2) for Q in np.geomspace(1, 1e4, 5).tolist()])
        obs_updates = observables.build(
            [
                "F2_charm",
                # "F2_bottom",
                # "F2_top",
                # "F2_light",
                # "F2_total",
            ],
            kins,
            update={
                "prDIS": [
                    "NC",
                    # "CC",
                ]
            },
        )
        return obs_updates

    def benchmark_ffn0(self, pto):
        self.run(
            self.theory_updates_ffn0(pto),
            self.obs_updates_ffn0(),
            ["ToyLH"],
        )


# ============================================================================ #
#                                  IC                                          #
# ============================================================================ #


class ApfelICBenchmark(ApfelBenchmark):
    """
    Globally set the external program to APFEL
    """

    @staticmethod
    def obs_updates(allow_cc=False):
        kinematics = []
        kinematics.extend([dict(x=x, Q2=10.0) for x in np.geomspace(1e-5, 1, 10)])
        kinematics.extend(
            [dict(x=0.1, Q2=Q2) for Q2 in np.geomspace(4, 20, 10).tolist()]
        )
        obs = [
            {
                "prDIS": "NC",
                "observables": {f: kinematics for f in ["F2_charm", "FL_charm"]},
            },
        ]
        if allow_cc:
            obs.append(
                {
                    "prDIS": "CC",
                    "observables": {
                        f: kinematics for f in ["F2_charm", "FL_charm", "F3_charm"]
                    },
                }
            )
        return obs


class BenchmarkICFFNS(ApfelICBenchmark):
    def benchmark_lo(self):
        self.run([{"IC": 1}], self.obs_updates(True), ["CT14llo_NF4"])

    def benchmark_nlo(self):
        self.run([{"PTO": 1, "IC": 1}], self.obs_updates(), ["CT14llo_NF4"])


if __name__ == "__main__":
    # plain = BenchmarkPlain()
    # plain.benchmark_pto(0)
    # plain.benchmark_pto(1)

    # proj = BenchmarkProjectile()
    # proj.benchmark_pto(0)
    # proj.benchmark_pto(1)

    # pos = BenchmarkPositivity()
    # pos.benchmark_pto(0)
    # pos.benchmark_pto(1)

    ffn0bench = BenchmarkFlavorNumberScheme()
    # ffn0bench.benchmark_zm(0)
    # ffn0bench.benchmark_zm(1)
    # ffn0bench.benchmark_zm(2)
    # ffn0bench.benchmark_ffns(1)
    # ffn0bench.benchmark_ffns(2)
    # ffn0bench.benchmark_ffn0(0)
    # ffn0bench.benchmark_ffn0(1)
    ffn0bench.benchmark_ffn0(2)

    # ffns = BenchmarkICFFNS()
    # ffns.benchmark_lo()
    # ffns.benchmark_nlo()

    # xs = BenchmarkXS()
    # xs.benchmark_pto(0)

    # pol = BenchmarkFlavorNumberScheme()
    # pol.benchmark_polarized(0)
    # pol.benchmark_polarized(1)

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
