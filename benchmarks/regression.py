# -*- coding: utf-8 -*-
#
# do regression test

import pytest

from db_interface import DBInterface


@pytest.mark.regression
class TestRegression:
    def _run(self, p, t_query):
        o_query = p.obs_query.noop()
        # p.run_generate_regression(t_query, o_query)
        p.run_queries_regression(t_query, o_query)

    def test_one_hot(self):
        p = DBInterface("regression.json")

        # test matrix
        features = {
            p.theory_query.XIR: [1.0, 2.0],
            p.theory_query.XIF: [1.0, 0.5],
            p.theory_query.TMC: [0, 1, 2, 3],
            p.theory_query.FNS: ["FFNS"],
            p.theory_query.NfFF: [3],
            p.theory_query.DAMP: [0],
        }
        # get the raw operator
        one_hot_query = p.theory_query.noop()
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
        self._run(p, one_hot_query)

    def test_FNS(self):
        p = DBInterface("regression.json")
        # test matrix
        features = {
            p.theory_query.XIR: [1.0],
            p.theory_query.XIF: [1.0],
            p.theory_query.TMC: [0],
        }
        # get the raw operator
        raw_query = p.theory_query.noop()
        for f, f_vals in features.items():
            raw_query &= f == f_vals[0]

        ffns_query = (
            (p.theory_query.FNS == "FFNS")
            & (p.theory_query.NfFF == 5)
            & (p.theory_query.DAMP == 0)
        )
        zm_vfns_query = (
            (p.theory_query.FNS == "ZM-VFNS")
            & p.theory_query.NfFF.one_of([3, 5])
            & (p.theory_query.DAMP == 0)
        )
        fonll_query = (
            p.theory_query.FNS.one_of(["FONLL-A"])
            & (p.theory_query.NfFF == 5)
            & p.theory_query.DAMP.one_of([0, 1])
        )
        total_query = raw_query & (ffns_query | zm_vfns_query | fonll_query)
        self._run(p, total_query)


if __name__ == "__main__":
    r = TestRegression()
    r.test_one_hot()
    r.test_FNS()
