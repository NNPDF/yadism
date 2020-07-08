# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

import pytest
from yadmark.db_interface import DBInterface, QueryFieldsEqual


class QCDNUMBenchmark:
    """Wrapper to apply some default settings"""
    db = None

    def _db(self):
        """init DB connection"""
        self.db = DBInterface("QCDNUM")
        return self.db

    def run_external(self, PTO, pdfs, theory_update=None, obs_query=None):
        """Query for PTO also in obs by default"""
        self._db()
        if obs_query is None:
            obs_query = self.db.obs_query.PTO == PTO
        return self.db.run_external(PTO, pdfs, theory_update, obs_query,)


@pytest.mark.quick_check
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
            {"FNS": ~(self.db.theory_query.FNS == "FONLL-A"), "NfFF": None},
        )

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

    def benchmark_NLO(self):
        self._benchmark_NLO_FFNS()
        self._benchmark_NLO_ZM_VFNS()


if __name__ == "__main__":
    plain = BenchmarkPlain()
    plain.benchmark_LO()
    # plain.benchmark_NLO()
