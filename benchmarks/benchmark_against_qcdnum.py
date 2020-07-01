# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest
from db_interface import DBInterface,QueryFieldsEqual


@pytest.mark.quick_check
class TestPlain:
    def test_LO(self):
        """
        Test the full LO order against QCDNUM
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

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
        # p.run_queries_external(t_query, o_query, ["toy_gonly"], "QCDNUM")

    def test_NLO(self):
        """
        Test the full NLO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
        # p.run_queries_external(t_query, o_query, ["toy_gonly"], "QCDNUM")

class TestScaleVar:
    # def test_LO(self, DBInterface):
    def test_LO(self):
        """
        Test the full LO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= QueryFieldsEqual("XIR","XIF")
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()
        # o_query |= p.obs_query.F2total.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
        # p.run_queries_external(t_query, o_query, ["toy_gonly"], "QCDNUM")

    def test_NLO(self):
        """
        Test the full NLO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= QueryFieldsEqual("XIR","XIF")
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
        # p.run_queries_external(t_query, o_query, ["toy_gonly"], "QCDNUM")


if __name__ == "__main__":
    plain = TestPlain()
    #plain.test_LO()
    #plain.test_NLO()

    sv = TestScaleVar()
    sv.test_LO()
    sv.test_NLO()
