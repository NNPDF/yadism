import numpy as np

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
    assert xs_coeffs("XSHERANCAVG", x=0.5, Q2=10, y=0.1)[2] == 0.0

    assert (
        xs_coeffs("XSHERANC", x=0.5, Q2=10, y=0.1, params=dict(projectilePID=-1))[0]
        == 1.0
    )

    heracc = xs_coeffs("XSHERACC", x=0.5, Q2=10, y=0.1, params=dict(projectilePID=1))
    assert heracc[0] + heracc[2] == 1 / 2.0

    chorus = xs_coeffs(
        "XSCHORUSCC",
        x=0.5,
        Q2=10,
        y=0.1,
        params=dict(projectilePID=1, M2target=0.0, M2W=1.0, GF=1.0),
    )
    assert all(chorus == np.array([0.0, 0.0, 0.0]))

    fw = xs_coeffs(
        "FW",
        x=0.5,
        Q2=1.0,
        y=0.1,
        params=dict(projectilePID=1, M2target=0.0, M2W=1.0),
    )
    assert fw[0] == 1.0
    assert fw[2] == 0.0

    f1 = xs_coeffs(
        "F1",
        x=1.0,
        Q2=1.0,
        y=0.0,
        params=dict(projectilePID=1, M2target=0.0, M2W=1.0),
    )
    assert f1[0] == 1.0
    assert f1[1] == -1.0
    assert f1[2] == 0.0

    xsfpfcc = xs_coeffs(
        "XSFPFCC",
        x=0.5,
        Q2=1.0,
        y=1.0,
        params=dict(projectilePID=1, M2target=0.0, M2W=1.0, GF=1.0),
    )
    assert xsfpfcc[0] == 3.893793e8 / (16.0 * 0.5 * np.pi)

    nutev = xs_coeffs(
        "XSNUTEVCC",
        x=0.5,
        Q2=1.0,
        y=0.1,
        params=dict(projectilePID=1, M2target=0.0, M2W=1.0),
    )
    assert nutev[0] + nutev[2] == 100.0 / 2**2


def test_alpha_qed():
    xs = XS("XSHERANC", MockRunner(MockCouplingConstants(-1)))
    assert (
        EXS(
            dict(x=0.5, Q2=10, y=0.1), xs.obs_name, xs.runner.configs, xs.get_esf
        ).alpha_qed_power()
        == 0.0
    )
