# -*- coding: utf-8 -*-
#
# do regression test

#import pytest

from conftest import DBInterface

class TestRegression:
    def test_one_hot(self):
        p = DBInterface()

        # test matrix
        features = {
            p.theory_query.XIR: [1.0, 2.0],
            p.theory_query.XIF: [1.0, 0.5],
            p.theory_query.TMC: [0, 1, 2, 3]
        }
        # get the raw operator
        raw_query = p.theory_query.noop()
        for f,f_vals in features.items():
            raw_query &= (f == f_vals[0])
        # activate one feature at a time
        for f,f_vals in features.items():
            # iterate the non-trivial values
            for v in f_vals[1:]:
                lower_query = (f == v)
                # make the others trivial
                for g,g_vals in features.items():
                    # skip myself
                    if f is g:
                        continue
                    lower_query &= (g == g_vals[0])
                raw_query |= lower_query

        o_query = p.obs_query.noop()

if __name__ == "__main__":
    r = TestRegression()
    r.test_one_hot()