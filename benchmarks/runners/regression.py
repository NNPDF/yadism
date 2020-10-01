# -*- coding: utf-8 -*-
#
# do regression test

import pytest

from yadmark.benchmark.db_interface import DBInterface


@pytest.mark.regression
class TestRegression:
    db = None

    def _db(self):
        self.db = DBInterface("regression")
        return self.db

    def _run(self, t_query):
        o_query = self.db.obs_query.noop()
        #o_query = ((self.db.obs_query.prDIS == "EM") & (self.db.obs_query.projectile == "electron") & (self.db.obs_query.PolarizationDIS == 0))
        self.db.run_generate_regression(t_query, o_query)
        #self.db.run_queries_regression(t_query, o_query)

    def test_one_hot(self):
        self._db()

        # test matrix
        features = {
            self.db.theory_query.XIR: [1.0, 2.0],
            self.db.theory_query.XIF: [1.0, 0.5],
            self.db.theory_query.TMC: [0, 1, 2, 3],
            self.db.theory_query.FNS: ["FFNS"],
            self.db.theory_query.NfFF: [3],
            self.db.theory_query.DAMP: [0],
        }
        # get the raw operator
        one_hot_query = self.db.theory_query.noop()
        for f, f_vals in features.items():
            one_hot_query &= f == f_vals[0]
        # activate one feature at a time
        for f, f_vals in features.items():
            # iterate the non-trivial values
            for v in f_vals[1:]:
                lower_query = f == v
                # make the others trivial
                for g, g_vals in features.items():
                    # skip myself
                    if f is g:
                        continue
                    lower_query &= g == g_vals[0]
                one_hot_query |= lower_query
        self._run(one_hot_query)

    def test_FNS(self):
        self._db()
        # test matrix
        features = {
            self.db.theory_query.XIR: [1.0],
            self.db.theory_query.XIF: [1.0],
            self.db.theory_query.TMC: [0],
            self.db.theory_query.PTO: [1],
        }
        # get the raw operator
        raw_query = self.db.theory_query.noop()
        for f, f_vals in features.items():
            raw_query &= f == f_vals[0]

        ffns_query = (
            (self.db.theory_query.FNS == "FFNS")
            & (self.db.theory_query.NfFF == 5)
            & (self.db.theory_query.DAMP == 0)
        )
        zm_vfns_query = (
            (self.db.theory_query.FNS == "ZM-VFNS")
            & self.db.theory_query.NfFF.one_of([3, 5])
            & (self.db.theory_query.DAMP == 0)
        )
        fonll_query = (
            self.db.theory_query.FNS.one_of(["FONLL-A"])
            & (self.db.theory_query.NfFF == 5)
            & self.db.theory_query.DAMP.one_of([0, 1])
        )
        total_query = raw_query & (ffns_query | zm_vfns_query | fonll_query)
        self._run(total_query)


if __name__ == "__main__":
    r = TestRegression()
    r.test_one_hot()
    r.test_FNS()
