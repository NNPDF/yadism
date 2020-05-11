# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from conftest import DBInterface


@pytest.mark.quick_check
class TestPlain:
    # def test_LO(self, DBInterface):
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = DBInterface()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query, ["ToyLH"])

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = DBInterface()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0

        o_query = p._obs_query.prDIS.exists()

        p.run_all_tests(t_query, o_query, ["ToyLH"])


@pytest.mark.commit_check
class TestScaleVariations:
    def test_LO(self):
        p = DBInterface()
        t_query = p._theory_query.PTO == 0

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query, ["CT14llo_NF3"])

    def test_NLO(self):
        p = DBInterface()
        t_query = p._theory_query.PTO == 1

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query, ["CT14llo_NF3"])


@pytest.mark.full
class TestFull:
    def test_LO(self):
        p = DBInterface()
        t_query = p._theory_query.PTO == 0

        o_query = p._obs_query.prDIS.exists()

        p.run_all_tests(t_query, o_query, ["ToyLH", "CT14llo_NF3"])

    def test_NLO(self):
        p = DBInterface()
        t_query = p._theory_query.PTO == 1

        o_query = p._obs_query.prDIS.exists()

        p.run_all_tests(t_query, o_query, ["ToyLH", "CT14llo_NF3"])


if __name__ == "__main__":
    plain = TestPlain()
    plain.test_LO()
    # plain.test_NLO()

    sv = TestScaleVariations()
    # sv.test_LO()
    # sv.test_NLO()

    f = TestFull()
    # f.test_LO()
