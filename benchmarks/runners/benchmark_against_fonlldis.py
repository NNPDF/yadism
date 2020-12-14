# -*- coding: utf-8 -*-
#
# Compare the results with FONLLdis

import pytest
from yadmark.benchmark.db_interface import DBInterface, QueryFieldsEqual
from yadmark.data import observables
from yadmark.data import theories


class FONLLdisBenchmark:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self, assert_external=None):
        """init DB connection"""
        self.db = DBInterface("FONLLdis", assert_external=assert_external)
        return self.db

    def run_external(
        self, PTO, pdfs, theory_update=None, obs_query=None, assert_external=None
    ):
        """Query for PTO also in obs by default"""
        self._db(False)
        return self.db.run_external(PTO, pdfs, theory_update)


@pytest.mark.quick_check
class BenchmarkPlain(FONLLdisBenchmark):
    """The most basic checks"""

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["CT14llo_NF4"],
            {
                "FNS": self._db().theory_query.FNS == "FONLL-A",
                "NfFF": self._db().theory_query.NfFF == 4,
            },
        )


class BenchmarkThreshold(FONLLdisBenchmark):
    """FONLL with threshold damping"""

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["CT14llo_NF4"],
            {
                "FNS": self._db().theory_query.FNS == "FONLL-A",
                "NfFF": self._db().theory_query.NfFF == 4,
                "DAMP": self.db.theory_query.DAMP == 1,
            },
        )


if __name__ == "__main__":

    sc = BenchmarkPlain()
    sc.benchmark_NLO()

    sc = BenchmarkThreshold()
    sc.benchmark_NLO()
