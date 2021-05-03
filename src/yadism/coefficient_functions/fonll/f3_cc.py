# -*- coding: utf-8 -*-

import numpy as np

from eko import constants

from . import partonic_channel as pc
from .. import splitting_functions as split
from ...esf.distribution_vec import rsl_from_distr_coeffs


class AsyQuark(pc.PartonicChannelAsy):
    # TODO this should be pure light

    def LO(self):
        return 0.0, 0.0, 1.0

    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z):
            return (
                CF
                * (
                    -(1.0 + z ** 2) / (1.0 - z) * np.log(z)
                    - (1.0 + z) * np.log(1.0 - z)
                    + (2.0 + z)
                )
                * as_norm
            )

        delta = -CF * (9.0 / 2.0 + np.pi ** 2 / 3.0) * as_norm

        omz_pd = -CF * 3.0 / 2.0 * as_norm

        log_pd = 2.0 * CF * as_norm

        return rsl_from_distr_coeffs(reg, delta, omz_pd, log_pd)

    def NLO_fact(self):
        return split.pqq_reg, split.pqq_sing, split.pqq_local


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z, L=self.L):
            return -(split.pqg(z) / 2.0) * L * as_norm

        return reg

    def NLO_fact(self):
        return split.pqg
