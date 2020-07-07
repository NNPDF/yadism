# -*- coding: utf-8 -*-
#
# Compare the results with QCDNUM

import pytest
from db_interface import DBInterface, QueryFieldsEqual


class QCDNUMBenchmark:
    db = None

    def _db(self):
        self.db = DBInterface("QCDNUM")
        return self.db


# @pytest.mark.quick_check
class BenchmarkPlain(QCDNUMBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self._db().run_external(0, ["ToyLH"])

    def benchmark_NLO(self):
        return self._db().run_external(1, ["ToyLH"])


class BenchmarkScaleVariations(QCDNUMBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self._db().run_external(
            0, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
        )

    def benchmark_NLO(self):
        return self._db().run_external(
            1, ["CT14llo_NF6"], {"XIR": QueryFieldsEqual("XIR", "XIF"), "XIF": None}
        )


class BenchmarkFNS(QCDNUMBenchmark):
    """Flavor Number Schemes"""

    def benchmark_LO(self):
        return self._db().run_external(
            0,
            ["CT14llo_NF6"],
            {"FNS": ~(self.db.theory_query.FNS == "FONLL-A"), "NfFF": None},
        )

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

    def benchmark_NLO(self):
        self._benchmark_NLO_FFNS()
        self._benchmark_NLO_ZM_VFNS()


if __name__ == "__main__":
    plain = BenchmarkPlain()
    plain.benchmark_LO()
    # plain.benchmark_NLO()
