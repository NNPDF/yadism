from yadism.esf.exs import EvaluatedCrossSection as EXS
from yadism.observable_name import ObservableName as ON
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


def test_f_coeffs():

    make_coeffs = lambda name: EXS(
        XS(ON(name), MockRunner(MockCouplingConstants(-1))),
        dict(x=0.5, Q2=10, y=0.1),
    ).f_coeffs()
    assert make_coeffs("XSHERANC")[0] == 1.0


def test_alpha_qed():
    assert (
        EXS(
            XS("XSHERANC", MockRunner(MockCouplingConstants(-1))),
            dict(x=0.5, Q2=10, y=0.1),
        ).alpha_qed_power()
        == 0.0
    )
