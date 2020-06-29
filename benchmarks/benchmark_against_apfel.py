# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

from db_interface import DBInterface


@pytest.mark.quick_check
class TestPlain:
    # def test_LO(self, DBInterface):
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()
        # o_query |= p.obs_query.F2total.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"])
        # p.run_queries_external(t_query, o_query, ["toy_gonly"])

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"])
        # p.run_queries_external(t_query, o_query, ["toy_gonly"])


@pytest.mark.commit_check
class TestScaleVariations:
    def test_LO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["CT14llo_NF3"])

    def test_NLO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.prDIS.exists()

        p.run_queries_external(t_query, o_query, ["CT14llo_NF3"])


@pytest.mark.commit_check
class TestTMC:
    def test_LO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC != 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"])
        # p.run_queries_external(t_query, o_query, ["uonly-dense"])

    def test_NLO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC != 0
        # t_query &= p.theory_query.TMC == 1

        o_query = p.obs_query.prDIS.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"])


class TestFNS:
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.TMC == 0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"

        o_query = p.obs_query.F2light.exists()

        # p.run_queries_external(t_query, o_query, ["CT14llo_NF6"])
        p.run_queries_external(t_query, o_query, ["uonly"])

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.TMC == 0
        t_query &= p.theory_query.NfFF == 4
        # t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.FNS == "FONLL-A"

        o_query = p.obs_query.F2charm.exists()

        # p.run_queries_external(t_query, o_query, ["gonly"])
        p.run_queries_external(t_query, o_query, ["CT14llo_NF6"])


class TestTMCFNS:
    def test_LO(self):
        """
        Test the full LO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.TMC == 2

        o_query = p.obs_query.prDIS.exists()

        p.run_queries_external(t_query, o_query, ["CT14llo_NF6"])
        # p.run_queries_external(t_query, o_query, ["gonly"])

    def test_NLO(self):
        """
        Test the full NLO order against APFEL's.
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.TMC == 2

        o_query = p.obs_query.prDIS.exists()

        # p.run_queries_external(t_query, o_query, ["gonly"])
        p.run_queries_external(t_query, o_query, ["CT14llo_NF6"])


@pytest.mark.full
class TestFull:
    def test_LO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0

        o_query = p.obs_query.prDIS.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH", "CT14llo_NF3"])

    def test_NLO(self):
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1

        o_query = p.obs_query.prDIS.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH", "CT14llo_NF3"])


if __name__ == "__main__":
    plain = TestPlain()
    plain.test_LO()
    plain.test_NLO()

    # sv = TestScaleVariations()
    # sv.test_LO()
    # sv.test_NLO()

    # tmc = TestTMC()
    # tmc.test_LO()
    # tmc.test_NLO()

    fns = TestFNS()
    # fns.test_LO()
    # fns.test_NLO()

    # tmc_fns = TestTMCFNS()
    # tmc_fns.test_LO()
    # tmc_fns.test_NLO
