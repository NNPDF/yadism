# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions

.. todo::
    docs
"""

import numpy as np

from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..esf import rsl_from_distr_coeffs


class F2asyQuark(pc.PartonicChannelAsy):
    """
        Computes the quark channel of the asymptotic limit of F2heavy.
    """

    label = "q"

    def LO(self):
        return 0, 0, 1

    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z):
            return (
                -CF * (1.0 + z ** 2) / (1.0 - z) * np.log(z)
                - CF * (1.0 + z) * np.log(1.0 - z)
                + CF * (3.0 + 2.0 * z)
            ) * as_norm

        delta = -CF * (9.0 / 2.0 + np.pi ** 2 / 3.0) * as_norm

        omz_pd = -CF * 3.0 / 2.0 * as_norm

        log_pd = 2 * CF * as_norm

        return rsl_from_distr_coeffs(reg, delta, omz_pd, log_pd)

    def NLO_fact(self):
        as_norm = 2.0

        def reg(z):
            return split.pqq_reg(z) * as_norm

        return rsl_from_distr_coeffs(reg, as_norm*split.pqq_delta(0), as_norm*split.pqq_pd(0))


class F2asyGluon(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of F2heavy.
    """

    label = "g"

    def NLO(self):
        as_norm = 2.0

        def reg(z, L=self.L):
            return (
                split.pqg(z) * (2.0 * np.log((1.0 - z) / z) + L)
                + 8.0 * z * (1.0 - z)
                - 1.0
            ) * as_norm

        return reg

    def NLO_fact(self):
        as_norm = 2.0 / 2.0 # TODO clashes with the 2 in esf

        def reg(z):
            return split.pqg(z) * as_norm

        return reg
