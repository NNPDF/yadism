# -*- coding: utf-8 -*-

import pytest

import yadism.splitting_functions as split


class MockConstants:
    def __init__(self, **kwargs):
        self.TF = kwargs.get("TF", 1.0)
        self.CF = kwargs.get("CF", 1.0)


class TestSplittingLO:
    def test_pqq(self):
        assert split.pqq_reg(-1, MockConstants()) == 0
        assert split.pqq_reg(0.35, MockConstants(CF=0)) == 0
        assert split.pqq_delta(0.15, MockConstants(CF=0)) == 0
        assert split.pqq_pd(0.05, MockConstants(CF=0)) == 0

    def test_pqg(self):
        assert split.pqg(0.61, MockConstants(TF=0)) == 0
