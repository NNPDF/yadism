# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from yadmark.db_interface import DBInterface


class ApfelBenchmark:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self,assert_external=None):
        """init DB connection"""
        self.db = DBInterface("APFEL",assert_external=assert_external)
        return self.db

    def run_external(self, PTO, pdfs, theory_update=None, obs_query=None, assert_external=None):
        """Query for PTO also in obs by default"""
        self._db(assert_external)
        if obs_query is None:
            obs_query = self.db.obs_query.PTO == PTO
        return self.db.run_external(PTO, pdfs, theory_update, obs_query,)


@pytest.mark.quick_check
class BenchmarkPlain(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(0, ["ToyLH"])

    def benchmark_NLO(self):
        def my_assert_external(theory, sf, yad):
            if sf == "FLbottom" and theory["mb"]**2/4 < yad["Q2"] < theory["mb"]**2:
                return dict(abs=2e-6)
            return None
        return self.run_external(1, ["ToyLH"],assert_external=my_assert_external)


@pytest.mark.commit_check
class BenchmarkScaleVariations(ApfelBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self.run_external(0, ["CT14llo_NF3"], {"XIR": None, "XIF": None})

    def benchmark_NLO(self):
        return self.run_external(1, ["CT14llo_NF3"], {"XIR": None, "XIF": None})


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
    plain = BenchmarkPlain()
    #plain.benchmark_LO()
    plain.benchmark_NLO()

    # sv = BenchmarkScaleVariations()
    # sv.benchmark_LO()
