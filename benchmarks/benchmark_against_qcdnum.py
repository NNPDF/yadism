# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest
from db_interface import DBInterface, QueryFieldsEqual


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

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")

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

        o_query = p.obs_query.F2charm.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")


class TestScaleVar:
    def test_LO(self):
        """
        Test the full LO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= QueryFieldsEqual("XIR", "XIF")
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")

    def test_NLO(self):
        """
        Test the full NLO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= QueryFieldsEqual("XIR", "XIF")
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")


class TestFNS:
    def test_LO(self):
        """
        Test the full LO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 0
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= ~(p.theory_query.FNS == "FONLL-A")
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")

    def run_NLO_FFNS(self):
        """
        Test the full NLO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.FNS == "FFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = ~p.obs_query.F2total.exists()
        o_query &= ~p.obs_query.FLtotal.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")

    def run_NLO_ZM_VFNS(self):
        """
        Test the full NLO order against QCDNUM
        """
        p = DBInterface("input.json")
        t_query = p.theory_query.PTO == 1
        t_query &= p.theory_query.XIR == 1.0
        t_query &= p.theory_query.XIF == 1.0
        t_query &= p.theory_query.NfFF == 3
        t_query &= p.theory_query.FNS == "ZM-VFNS"
        t_query &= p.theory_query.TMC == 0

        o_query = p.obs_query.F2light.exists()
        o_query |= p.obs_query.FLlight.exists()

        p.run_queries_external(t_query, o_query, ["ToyLH"], "QCDNUM")

    def test_NLO(self):
        self.run_NLO_FFNS()
        self.run_NLO_ZM_VFNS()


if __name__ == "__main__":
    plain = TestPlain()
    #plain.test_LO()
    plain.test_NLO()

    sv = TestScaleVar()
    # sv.test_LO()
    # sv.test_NLO()

    fns = TestFNS()
    # fns.test_LO()
    # fns.test_NLO()
