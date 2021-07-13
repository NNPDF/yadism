# -*- coding: utf-8 -*-

from unittest import mock

from yadism.coefficient_functions.splitting_functions import lo


class TestSplittingLO:
    def test_pqq(self):
        assert lo.pqq_reg(-1, [3]) == 0
        with mock.patch("eko.constants.CF", 0):
            assert lo.pqq_reg(0.35, [3]) == 0
            assert lo.pqq_sing(0.35, [3]) == 0
            assert lo.pqq_local(0.35, [3]) == 0

    def test_pqg(self):
        with mock.patch("eko.constants.TR", 0):
            assert lo.pqg_reg(0.61, [3]) == 0
