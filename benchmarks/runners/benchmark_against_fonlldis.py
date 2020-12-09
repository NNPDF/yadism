# -*- coding: utf-8 -*-
#
# Compare the results with FONLLdis

import pytest
from yadmark.benchmark.db_interface import DBInterface, QueryFieldsEqual


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
        self._db(assert_external)
        if obs_query is None:
            obs_query = self.db.obs_query.PTO == PTO
            if (
                PTO > 0
            ):  # by default we're running in FFNS3, so we can use the big runcard
                obs_query &= self.db.obs_query.F2charm.exists()
        return self.db.run_external(PTO, pdfs, theory_update, obs_query,)


@pytest.mark.quick_check
@pytest.mark.commit_check
class BenchmarkPlain(FONLLdisBenchmark):
    """The most basic checks"""

    def benchmark_NLO(self):
        return self.run_external(
            1, 
            ["CT14llo_NF4"],
            {"FNS": ~(self._db().theory_query.FNS == "FONLL-A")})

class BenchmarkThreshold(FONLLdisBenchmark):
    """FONLL with threshold damping"""

    def benchmark_NLO(self):
        return self.run_external(
            1, 
            ["ToyLH"],
            {
                "FNS": ~(self._db().theory_query.FNS == "FONLL-A"),
                "DAMP": self.db.theory_query.DAMP == 1
            })


if __name__ == "__main__":

    sc = BenchmarkPlain()
    sc.benchmark_NLO()

    sc = BenchmarkThreshold()
    sc.benchmark_NLO()