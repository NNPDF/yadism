# pylint: disable=attribute-defined-outside-init

import copy

import numpy as np
import pytest

from yadism.coefficient_functions.intrinsic import partonic_channel, raw_nc


class MockObj:
    pass


def test_li2():
    assert raw_nc.li2(0) == 0
    assert raw_nc.li2(1) == np.pi**2 / 6.0


def test_Cplus():
    pc = MockObj()
    pc.m1sq = np.random.rand()
    pc.m2sq = 0
    pc.I1 = np.random.rand()
    assert raw_nc.Cplus(pc) == 0
    pc.m2sq = np.random.rand()
    pc.m1sq = 0
    assert raw_nc.Cplus(pc) == 0


def test_C1pm():
    pc = MockObj()
    pc.sigma_pm = pc.sigma_mp = np.random.rand()
    pc.m1sq = pc.m2sq = np.random.rand()
    pc.I1 = np.random.rand()
    pc.Q2 = np.random.rand()
    assert raw_nc.C1p(pc) == raw_nc.C1m(pc)


def test_S():
    pc = MockObj()
    pc.sigma_pp = np.random.rand()
    pc.delta = np.random.rand()
    pc.I1 = np.random.rand()
    pc.Q2 = np.random.rand()
    pc.m2sq = np.random.rand()
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.m2sq = 0
        raw_nc.S(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.Q2 = 0
        raw_nc.S(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.delta = 0
        raw_nc.S(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.delta = ppc.sigma_pp
        raw_nc.S(ppc)


def test_CRm():
    pc = MockObj()
    pc.sigma_pp = np.random.rand()
    pc.sigma_pm = np.random.rand()
    pc.sigma_mp = np.random.rand()
    pc.delta = np.random.rand()
    pc.I1 = np.random.rand()
    pc.Q2 = np.random.rand()
    pc.m1sq = np.random.rand()
    pc.m2sq = np.random.rand()
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.m1sq = 0
        with pytest.warns(RuntimeWarning):
            raw_nc.CRm(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.m2sq = 0
        raw_nc.CRm(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.Q2 = 0
        raw_nc.CRm(ppc)
    with pytest.raises(ZeroDivisionError):
        ppc = copy.copy(pc)
        ppc.delta = 0
        raw_nc.CRm(ppc)
    with pytest.warns(RuntimeWarning):
        ppc = copy.copy(pc)
        ppc.delta = ppc.sigma_pm
        assert not np.isfinite(raw_nc.CRm(ppc))
    with pytest.warns(RuntimeWarning):
        ppc = copy.copy(pc)
        ppc.delta = ppc.sigma_mp
        assert not np.isfinite(raw_nc.CRm(ppc))
    pc.sigma_pp = 0  # deny contributions
    pc.Q2 = pc.m1sq = pc.m2sq
    pc.delta = partonic_channel.NeutralCurrentBase.kinematic_delta(
        pc.m1sq, pc.m2sq, -pc.Q2
    )
    pc.sigma_mp *= pc.delta  # Sigma_mp < delta otherwise the Li2 become undefined
    pc.sigma_pm *= pc.delta  # see above
    pc.I1 = 1.0
    assert pytest.approx(raw_nc.CRm(pc)) == 5.0 / 2.0 * pc.Q2 - 4.0
