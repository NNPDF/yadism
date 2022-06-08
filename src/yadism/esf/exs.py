# -*- coding: utf-8 -*-
import numpy as np

from ..observable_name import ObservableName
from .esf import ESFInfo
from .result import ESFResult, EXSResult

GEV_CM2_CONV = 3.893793e10
"Conversion factor from GeV^-2 to 10^-38 cm^2"


def xs_coeffs(kind, y, x=None, Q2=None, params=None):
    """Compute coefficients in the definition of a given cross section.

    Parameters
    ----------
    kind : str
        the identifier of the cross section for which coefficients have to be
        computed
    y : float
        Bjorken y value for the chosen kinematic point
    x: None or float
        Bjorken x value for the chosen kinematic point
    Q2: None or float
        photon virtuality for the chosen kinematic point
    params : None or dict
        theory parameters required to fully specify the coefficients (which ones
        depends on the chosen definition, i.e. on `kind`)

    Returns
    -------
    np.ndarray
        the coefficients of the cross-section on the basis `(F2, FL, xF3)`

    Raises
    ------
    ValueError or KeyError
        in case not enough parameters have been specified

    """
    yp = 1.0 + (1.0 - y) ** 2
    ym = 1.0 - (1.0 - y) ** 2
    yL = y**2

    # Neutral Currents
    # HERA average
    if kind == "XSHERANCAVG":
        return np.array([1.0, -yL / yp, 0.0])

    if params is None:
        raise ValueError(f"Parameters required to compute '{kind}' cross section.")

    f3sign = -1 if params["projectilePID"] < 0 else 1
    # HERA fixed lepton
    if kind == "XSHERANC":
        return np.array([1.0, -yL / yp, f3sign * ym / yp])

    # Charged Currents
    norm = 0.0
    # HERA
    if kind == "XSHERACC":
        norm = 1.0 / 4.0
    # FW CDHSW see http://cds.cern.ch/record/200223/files/198909396.pdf
    elif kind == "FW":
        mn = np.sqrt(params["M2target"])
        norm = 1.0
        ym = 0
        yp = 1.0
        yL = y**2 / (2 * (y**2 / 2 + (1 - y) - (mn * x * y) ** 2 / Q2))
    else:
        mn = np.sqrt(params["M2target"])
        m2w = params["M2W"]
        yp -= 2.0 * (mn * x * y) ** 2 / Q2  # = ypc
        # CHORUS
        if kind == "XSCHORUSCC":
            norm = (
                GEV_CM2_CONV
                * params["GF"] ** 2
                * mn
                / (2.0 * np.pi * (1.0 + Q2 / m2w) ** 2)
            )
        # NUTEV
        if kind == "XSNUTEVCC":
            norm = 100.0 / 2.0 / (1.0 + Q2 / m2w) ** 2
    return np.array([yp, -yL, f3sign * ym]) * norm


class EvaluatedCrossSection:
    def __init__(self, kin, obs_name, configs, get_esf):
        self.kin = kin
        self.Q2 = kin["Q2"]
        self.x = kin["x"]
        self.y = kin["y"]
        self.info = ESFInfo(obs_name, configs)
        self.get_esf = get_esf

    def alpha_qed_power(self):
        return 0

    def get_result(self):
        # Collect esfs
        flavor = self.info.obs_name.flavor
        f_coeffs = xs_coeffs(
            self.info.obs_name.kind,
            self.y,
            x=self.x,
            Q2=self.Q2,
            params=dict(
                projectilePID=self.info.configs.coupling_constants.obs_config[
                    "projectilePID"
                ],
                M2target=self.info.configs.M2target,
                M2W=self.info.configs.M2W,
                GF=self.info.configs.GF,
            ),
        )
        f2 = self.get_esf(ObservableName(f"F2_{flavor}"), self.kin).get_result()
        fl = self.get_esf(ObservableName(f"FL_{flavor}"), self.kin).get_result()
        # skip F3 if it is not required
        if f_coeffs[2] != 0.0:
            f3 = self.get_esf(ObservableName(f"F3_{flavor}"), self.kin).get_result()
        else:
            f3 = ESFResult(self.x, self.Q2, f2.nf)

        # add normalizations
        esf = f_coeffs @ np.array([f2, fl, f3])
        # remap to EXS
        sigma = EXSResult(self.x, self.Q2, self.y, f2.nf)
        for o, v in esf.orders.items():
            # now shift orders: push alpha_qed two powers up
            sigma.orders[(o[0], o[1] + self.alpha_qed_power(), o[2], o[3])] = v
        return sigma
