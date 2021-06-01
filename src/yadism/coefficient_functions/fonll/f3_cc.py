# -*- coding: utf-8 -*-

import numpy as np

from eko import constants

from . import partonic_channel as pc
from ..partonic_channel import RSL, EmptyPartonicChannel
from ..intrinsic import f3_cc


class AsyQuark(pc.PartonicChannelAsy):
    # TODO this should be pure light

    def LO(self):
        return RSL.from_delta(1.0)

    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z, _args):
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

        return RSL.from_distr_coeffs(reg, (delta, omz_pd, log_pd))


class AsyGluon(EmptyPartonicChannel):
    pass


class MatchingIntrinsicRplus(pc.FMatchingQuarkCC):
    ffns = f3_cc.Rplus
