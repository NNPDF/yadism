# -*- coding: utf-8 -*-
import numpy as np

from ..observable_name import ObservableName
from .esf import ESFInfo
from .result import ESFResult, EXSResult

conv = 3.893793e10  # conversion factor from GeV^-2 to 10^-38 cm^2


class EvaluatedCrossSection:
    def __init__(self, kin, obs_name, configs, get_esf):
        self.kin = kin
        self.info = ESFInfo(obs_name, configs)
        self.get_esf = get_esf

    def f_coeffs(self):
        y = self.kin["y"]
        yp = 1.0 + (1.0 - y) ** 2
        ym = 1.0 - (1.0 - y) ** 2
        yL = y**2
        obs_config = self.info.configs.coupling_constants.obs_config
        f3sign = -1 if obs_config["projectilePID"] < 0 else 1
        # eta = 1 if obs_config["process"] == "CC" else 1
        # the alpha_qed^2 part is shifted below
        # norm = 2.0 * np.pi / (y * x * Q2)
        kind = self.info.obs_name.kind
        # if kind == "XSreduced":
        #     return np.array([1.0, -yL / yp, f3sign * ym / yp])
        # if kind == "XSyreduced":
        #     return np.array([yp, -yL, f3sign * ym])
        if kind == "XSHERANCAVG":
            return np.array([1.0, -yL / yp, 0.0])
        if kind == "XSHERANC":
            return np.array([1.0, -yL / yp, f3sign * ym / yp])
        norm = 0.0
        if kind == "XSHERACC":
            norm = 1.0 / 4.0
        else:
            x = self.kin["x"]
            Q2 = self.kin["Q2"]
            mn = np.sqrt(self.info.configs.M2target)
            m2w = self.info.configs.M2W
            yp -= 2.0 * (mn * x * y) ** 2 / Q2  # = ypc
            # Chorus
            if kind == "XSCHORUSCC":
                norm = (
                    conv
                    * self.info.configs.GF**2
                    * mn
                    / (2.0 * np.pi * (1.0 + Q2 / m2w) ** 2)
                )
            if kind == "XSNUTEVCC":
                norm = 100.0 / 2.0 / (1.0 + Q2 / m2w) ** 2
        return np.array([yp, -yL, f3sign * ym]) * norm

    def alpha_qed_power(self):
        return 0

    def get_result(self):
        # Collect esfs
        flavor = self.info.obs_name.flavor
        f_coeffs = self.f_coeffs()
        f2 = self.get_esf(ObservableName(f"F2_{flavor}"), self.kin).get_result()
        fl = self.get_esf(ObservableName(f"FL_{flavor}"), self.kin).get_result()
        # skip F3 if it is not required
        if f_coeffs[2] != 0.0:
            f3 = self.get_esf(ObservableName(f"F3_{flavor}"), self.kin).get_result()
        else:
            f3 = ESFResult(self.kin["x"], self.kin["Q2"], f2.nf)

        # add normalizations
        esf = f_coeffs @ np.array([f2, fl, f3])
        # remap to EXS
        sigma = EXSResult(self.kin["x"], self.kin["Q2"], self.kin["y"], f2.nf)
        for o, v in esf.orders.items():
            # now shift orders: push alpha_qed two powers up
            sigma.orders[(o[0], o[1] + self.alpha_qed_power(), o[2], o[3])] = v
        return sigma
