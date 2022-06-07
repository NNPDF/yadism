# -*- coding: utf-8 -*-
from yadism.esf.exs import EvaluatedCrossSection as EXS
from yadism.esf.exs import xs_coeffs
from yadism.xs import CrossSection as XS


class MockRunnerConfigs:
    def __init__(self, coupling_constants):
        self.coupling_constants = coupling_constants


class MockRunner:
    def __init__(self, coupling_constants):
        self.configs = MockRunnerConfigs(coupling_constants=coupling_constants)


class MockCouplingConstants:
    def __init__(self, f3sign):
        self.obs_config = dict(projectilePID=f3sign)


def test_xs_coeffs():
    assert (
        xs_coeffs("XSHERANC", x=0.5, Q2=10, y=0.1, params=dict(projectilePID=-1))[0]
        == 1.0
    )


def test_alpha_qed():
    xs = XS("XSHERANC", MockRunner(MockCouplingConstants(-1)))
    assert (
        EXS(
            dict(x=0.5, Q2=10, y=0.1), xs.obs_name, xs.runner.configs, xs.get_esf
        ).alpha_qed_power()
        == 0.0
    )
