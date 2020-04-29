# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from conftest import ParentTest


@pytest.mark.skip
class TestPlain:
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0
        t_query &= p._theory_query.PDFSet == "ToyLH"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.XIR == 1.0
        t_query &= p._theory_query.XIF == 1.0
        t_query &= p._theory_query.PDFSet == "ToyLH"

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)


@pytest.mark.skip
class TestScaleVariations:
    def test_LO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.PDFSet == "CT14llo_NF3"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.PDFSet == "CT14llo_NF3"

        o_query = p._obs_query.F2light.exists()

        p.run_all_tests(t_query, o_query)


class TestFull:
    def test_LO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 0
        t_query &= p._theory_query.PDFSet.one_of(["ToyLH", "CT14llo_NF3"])

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)

    def test_NLO(self):
        p = ParentTest()
        t_query = p._theory_query.PTO == 1
        t_query &= p._theory_query.PDFSet.one_of(["ToyLH", "CT14llo_NF3"])

        o_query = p._obs_query

        p.run_all_tests(t_query, o_query)


if __name__ == "__main__":
    plain = TestPlain()
    plain.test_LO()
    # plain.test_NLO()

    sv = TestScaleVariations()
    # sv.test_LO()
    # sv.test_NLO()
