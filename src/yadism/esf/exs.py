import numpy as np

from ..observable_name import ObservableName
from .esf_result import EXSResult


class EvaluatedCrossSection:
    def __init__(self, xs, kin):
        self.xs = xs
        self.kin = kin

    def get_result(self):
        # Collect esfs
        f2 = self.xs.get_esf(ObservableName("F2total"), self.kin).get_result()
        fl = self.xs.get_esf(ObservableName("FLtotal"), self.kin).get_result()
        f3 = self.xs.get_esf(ObservableName("F3total"), self.kin).get_result()
        # add normalizations
        x = self.kin["x"]
        Q2 = self.kin["Q2"]
        y = self.kin["y"]
        yp = 1.0 + (1.0 - y) ** 2
        ym = 1.0 - (1.0 - y) ** 2
        yL = y ** 2
        obs_config = self.xs.runner.managers["coupling_constants"].obs_config
        f3sign = -1 if obs_config["projectilePID"] < 0 else 1
        eta = 1 if obs_config["process"] == "CC" else 1
        # the alpha_qed^2 part is shifted below
        norm = 2.0 * np.pi / (y * x * Q2)
        esf = norm * eta * (yp * f2 + f3sign * ym * f3 - yL * fl)
        # remap to EXS
        sigma = EXSResult(x, Q2, y)
        for o, v in esf.orders.items():
            # now shift orders: push alpha_qed two powers up
            sigma.orders[(o[0], o[1] + 2, o[2], o[3])] = v
        return sigma
