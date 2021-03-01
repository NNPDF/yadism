import numpy as np

from ..observable_name import ObservableName
from .esf_result import EXSResult


class EvaluatedCrossSection:
    def __init__(self, xs, kin):
        self.xs = xs
        self.kin = kin

    def f_coeffs(self):
        # x = self.kin["x"]
        # Q2 = self.kin["Q2"]
        y = self.kin["y"]
        yp = 1.0 + (1.0 - y) ** 2
        ym = 1.0 - (1.0 - y) ** 2
        yL = y ** 2
        obs_config = self.xs.runner.managers["coupling_constants"].obs_config
        f3sign = -1 if obs_config["projectilePID"] < 0 else 1
        # eta = 1 if obs_config["process"] == "CC" else 1
        # the alpha_qed^2 part is shifted below
        # norm = 2.0 * np.pi / (y * x * Q2)
        return np.array([1.0, -yL / yp, f3sign * ym / yp])

    def alpha_qed_power(self):
        return 0

    def get_result(self):
        # Collect esfs
        flavor = self.xs.obs_name.flavor
        f2 = self.xs.get_esf(ObservableName(f"F2_{flavor}"), self.kin).get_result()
        fl = self.xs.get_esf(ObservableName(f"FL_{flavor}"), self.kin).get_result()
        f3 = self.xs.get_esf(ObservableName(f"F3_{flavor}"), self.kin).get_result()
        # add normalizations
        esf = self.f_coeffs() @ np.array([f2, fl, f3])
        # remap to EXS
        sigma = EXSResult(self.kin["x"], self.kin["Q2"], self.kin["y"])
        for o, v in esf.orders.items():
            # now shift orders: push alpha_qed two powers up
            sigma.orders[(o[0], o[1] + self.alpha_qed_power(), o[2], o[3])] = v
        return sigma
