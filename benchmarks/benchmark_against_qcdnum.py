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

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
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

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")
        # p.run_queries_external(t_query, o_query, ["toy_gonly"])


if __name__ == "__main__":
    plain = TestPlain()
    plain.test_LO()
    plain.test_NLO()
