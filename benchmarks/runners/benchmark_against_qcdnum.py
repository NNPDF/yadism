# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

import pytest
from yadmark.benchmark.db_interface import DBInterface, QueryFieldsEqual


class QCDNUMBenchmark:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self):
        """init DB connection"""
        self.db = DBInterface("QCDNUM", assert_external=False)
        return self.db

    def run_external(self, PTO, pdfs, theory_update=None, obs_query=None):
        """Query for PTO also in obs by default"""
        self._db()
        if obs_query is None:
            obs_query = self.db.obs_query.PTO == PTO
            if (
                PTO > 0
            ):  # by default we're running in FFNS3, so we can use the big runcard
                obs_query &= self.db.obs_query.F2charm.exists()
        return self.db.run_external(PTO, pdfs, theory_update, obs_query,)


@pytest.mark.quick_check
@pytest.mark.commit_check
class BenchmarkPlain(QCDNUMBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(0, ["ToyLH"])

    def benchmark_NLO(self):
        return self.run_external(1, ["ToyLH"])


class BenchmarkScaleVariations(QCDNUMBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self.run_external(
            0, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
        )

    def benchmark_NLO(self):
        return self.run_external(
            1, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
        )


class BenchmarkFNS(QCDNUMBenchmark):
    """Flavor Number Schemes"""

    def benchmark_LO(self):
        return self.run_external(
            0,
            ["CT14llo_NF6"],
            {"FNS": ~(self._db().theory_query.FNS == "FONLL-A"), "NfFF": None},
        )

    def _benchmark_NLO_FFNS3(self):
        self._db()
        return self.db.run_external(
            1,
            ["CT14llo_NF6"],
            {
                "FNS": self.db.theory_query.FNS == "FFNS",
                "NfFF": self.db.theory_query.NfFF == 3,
            },
            (self.db.obs_query.PTO == 1) & (self.db.obs_query.F2charm.exists()),
        )

    def _benchmark_NLO_FFNS4(self):
        self._db()
        return self.db.run_external(
            1,
            ["CT14llo_NF6"],
            {
                "FNS": self.db.theory_query.FNS == "FFNS",
                "NfFF": self.db.theory_query.NfFF == 4,
            },
            (self.db.obs_query.PTO == 1)
            & (self.db.obs_query.F2bottom.exists())
            & (~(self.db.obs_query.F2charm.exists())),
        )

    def _benchmark_NLO_FFNS5(self):
        self._db()
        return self.db.run_external(
            1,
            ["CT14llo_NF6"],
            {
                "FNS": self.db.theory_query.FNS == "FFNS",
                "NfFF": self.db.theory_query.NfFF == 5,
            },
            (self.db.obs_query.PTO == 1)
            & (self.db.obs_query.F2top.exists())
            & (~(self.db.obs_query.F2bottom.exists())),
        )

    def _benchmark_NLO_ZM_VFNS(self):
        self._db()
        return self.db.run_external(
            1,
            ["CT14llo_NF6"],
            {"FNS": self.db.theory_query.FNS == "ZM-VFNS"},
            (self.db.obs_query.PTO == 1)
            & (self.db.obs_query.F2light.exists())
            & (~(self.db.obs_query.F2charm.exists())),
        )

    def benchmark_NLO(self):
        self._benchmark_NLO_FFNS3()
        self._benchmark_NLO_FFNS4()
        self._benchmark_NLO_FFNS5()
        self._benchmark_NLO_ZM_VFNS()


if __name__ == "__main__":
    # plain = BenchmarkPlain()
    # plain.benchmark_LO()
    # plain.benchmark_NLO()

    # fns = BenchmarkFNS()
    # fns._benchmark_NLO_FFNS5()

    sc = BenchmarkScaleVariations()
    sc.benchmark_LO()
