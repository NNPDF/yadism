# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from yadmark.benchmark.db_interface import DBInterface


class ApfelBenchmark:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self, assert_external=None):
        """init DB connection"""
        self.db = DBInterface("APFEL", assert_external=assert_external)
        return self.db

    def run_external(
        self, PTO, pdfs, theory_update=None, obs_update=None, assert_external=None
    ):
        """Query for PTO also in obs by default"""
        self._db(assert_external)
        # set some defaults
        obs_matrix = {
            "PTO": self.db.obs_query.PTO == PTO,
            "prDIS": self.db.obs_query.prDIS == "EM",
            "projectile": self.db.obs_query.projectile == "electron",
            "PolarizationDIS": self.db.obs_query.PolarizationDIS == 0,
        }
        # allow changes
        if obs_update is not None:
            obs_matrix.update(obs_update)
        # collect Query
        obs_query = self.db.obs_query.noop()
        for q in obs_matrix.values():
            if q is None:
                continue
            obs_query &= q
        return self.db.run_external(PTO, pdfs, theory_update, obs_query)


@pytest.mark.quick_check
@pytest.mark.commit_check
class BenchmarkPlain(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(0, ["ToyLH"], obs_update={"prDIS": None})

    def benchmark_NLO(self):
        def my_assert_external(theory, obs, sf, yad):
            if (
                sf == "FLbottom"
                and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2
            ):
                return dict(abs=2e-6)
            elif obs["prDIS"] == "CC":
                if sf[2:] == "charm" and yad["x"] > 0.75:
                    return dict(abs=2e-6)
                if sf[2:] == "top" and yad["Q2"] < 150:
                    return dict(abs=1e-4)
            return None

        return self.run_external(
            1, ["ToyLH"], obs_update={"prDIS": None}, assert_external=my_assert_external
        )


@pytest.mark.commit_check
class BenchmarkProjectile(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(
            0,
            ["ToyLH"],
            obs_update={
                "prDIS": self._db().obs_query.prDIS.one_of(["NC", "CC"]),
                "projectile": None,
                "PolarizationDIS": None,
            },
        )

    def benchmark_NLO(self):
        def my_assert_external(theory, obs, sf, yad):
            if (
                sf == "FLbottom"
                and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2
            ):
                return dict(abs=2e-6)
            elif obs["prDIS"] == "CC":
                if sf[2:] == "charm" and yad["x"] > 0.75:
                    return dict(abs=2e-6)
                if sf[2:] == "top" and yad["Q2"] < 150:
                    return dict(abs=1e-4)
            return None

        return self.run_external(
            1,
            ["ToyLH"],
            obs_update={
                "prDIS": self._db().obs_query.prDIS.one_of(["NC", "CC"]),
                "projectile": None,
                "PolarizationDIS": None,
            },
            assert_external=my_assert_external,
        )


@pytest.mark.commit_check
class BenchmarkScaleVariations(ApfelBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self.run_external(
            0, ["CT14llo_NF3"], {"XIR": None, "XIF": None}, {"prDIS": None}
        )

    def benchmark_NLO(self):
        return self.run_external(
            1, ["CT14llo_NF3"], {"XIR": None, "XIF": None}, {"prDIS": None}
        )


@pytest.mark.commit_check
class BenchmarkTMC(ApfelBenchmark):
    """Add Target Mass Corrections"""

    def benchmark_LO(self):
        return self.run_external(0, ["ToyLH"], {"TMC": None})

    def benchmark_NLO(self):
        return self.run_external(1, ["ToyLH"], {"TMC": None})


class BenchmarkFNS(ApfelBenchmark):
    """Flavor Number Schemes"""

    def benchmark_LO(self):
        return self.run_external(0, ["CT14llo_NF6"], {"FNS": None, "NfFF": None})

    def _benchmark_NLO_FFNS(self):
        return self.run_external(
            1,
            ["CT14llo_NF6"],
            {"FNS": self.db.theory_query.FNS == "FFNS", "NfFF": None},
        )

    def _benchmark_NLO_ZM_VFNS(self):
        return self.run_external(
            1, ["CT14llo_NF6"], {"FNS": self.db.theory_query.FNS == "ZM-VFNS"}
        )

    def _benchmark_NLO_FONLL(self):
        return self.run_external(
            1,
            ["CT14llo_NF6"],
            {"FNS": self.db.theory_query.FNS == "FONLL-A", "DAMP": None},
        )

    def benchmark_NLO(self):
        self._benchmark_NLO_FFNS()
        self._benchmark_NLO_ZM_VFNS()
        self._benchmark_NLO_FONLL()


if __name__ == "__main__":
    # plain = BenchmarkPlain()
    # plain.benchmark_LO()
    # plain.benchmark_NLO()

    proj = BenchmarkProjectile()
    proj.benchmark_LO()
    # proj.benchmark_NLO()
