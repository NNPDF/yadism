# -*- coding: utf-8 -*-

import numpy as np

from eko import constants

from . import partonic_channel as pc
from .. import splitting_functions as split
from ..partonic_channel import RSL


class AsyQuark(pc.PartonicChannelAsy):
    # TODO inherit from light
    def LO(self):
        return RSL.from_delta(1.0)

    def NLO(self):
        CF = constants.CF
        as_norm = 2.0
        zeta_2 = np.pi ** 2 / 6.0

        def reg(z, args):
            return (
                CF
                * (
                    -(1.0 + z ** 2) / (1.0 - z) * np.log(z)
                    - (1.0 + z) * np.log(1.0 - z)
                    + (3.0 + 2.0 * z)
                )
                * as_norm
            )

        delta = -CF * (9.0 / 2.0 + 2.0 * zeta_2) * as_norm

        omz_pd = -CF * 3.0 / 2.0 * as_norm

        log_pd = 2.0 * CF * as_norm

        return RSL.from_distr_coeffs(reg, (delta, omz_pd, log_pd))

    def NLO_fact(self):
        return split.pqq_reg, split.pqq_sing, split.pqq_local


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z, args):
            L = self.L
            return (
                (split.pqg(z) / 2.0) * (2.0 * np.log((1.0 - z) / z) + L)
                + 8.0 * z * (1.0 - z)
                - 1.0
            ) * as_norm

        return RSL(reg)

    def NLO_fact(self):
        return split.pqg
