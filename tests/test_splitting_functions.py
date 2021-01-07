# -*- coding: utf-8 -*-

from unittest import mock
import pytest

import yadism.splitting_functions as split


class TestSplittingLO:
    def test_pqq(self):
        assert split.pqq_reg(-1) == 0
        with mock.patch("eko.constants.CF", 0):
            assert split.pqq_reg(0.35) == 0
            assert split.pqq_sing(0.35) == 0
            assert split.pqq_local(0.35) == 0

    def test_pqg(self):
        with mock.patch("eko.constants.TR", 0):
            assert split.pqg(0.61) == 0
