# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from db_interface import DBInterface


class ApfelBenchmark:
    db = None

    def _db(self):
        self.db = DBInterface()
        return self.db


@pytest.mark.quick_check
class BenchmarkPlain(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self._db().run_external(
            0,
            ["ToyLH"],
            None,
            obs_query=(
                self.db.obs_query.F2light.exists() | self.db.obs_query.F2total.exists()
            ),
        )

    def benchmark_NLO(self):
        return self._db().run_external(
            1,
            ["ToyLH"],
            None,
            obs_query=(
                ~(
                    self.db.obs_query.F2total.exists()
                    | self.db.obs_query.FLtotal.exists()
                )
            ),
        )


@pytest.mark.commit_check
class BenchmarkScaleVariations(ApfelBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self._db().run_external(0, ["CT14llo_NF3"], {"XIR": None, "XIF": None})

    def benchmark_NLO(self):
        return self._db().run_external(1, ["CT14llo_NF3"], {"XIR": None, "XIF": None})


@pytest.mark.commit_check
class BenchmarkTMC(ApfelBenchmark):
    """Add Target Mass Corrections"""

    def benchmark_LO(self):
        return self._db().run_external(0, ["ToyLH"], {"TMC": None})

    def benchmark_NLO(self):
        return self._db().run_external(1, ["ToyLH"], {"TMC": None})


class BenchmarkFNS(ApfelBenchmark):
    """Flavor Number Schemes"""

    def benchmark_LO(self):
        return self._db().run_external(0, ["CT14llo_NF6"], {"FNS": None, "NfFF": None})

    def _benchmark_NLO_FFNS(self):
        return self._db().run_external(
            1,
            ["CT14llo_NF6"],
            {"FNS": self.db.theory_query.FNS == "FFNS", "NfFF": None},
        )

    def _benchmark_NLO_ZM_VFNS(self):
        return self._db().run_external(
            1, ["CT14llo_NF6"], {"FNS": self.db.theory_query.FNS == "ZM-VFNS"}
        )

    def _benchmark_NLO_FONLL(self):
        return self._db().run_external(
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
    # plain.benchmark_LO()
    # plain.benchmark_NLO()

    sv = BenchmarkScaleVariations()
    sv.benchmark_LO()
