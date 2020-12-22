# -*- coding: utf-8 -*-

import numpy as np
from eko import constants

from ..partonic_channel import PartonicChannelHeavyIntrinsic
from .. import ic
from ..esf.distribution_vec import rsl_from_distr_coeffs


class F2IntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.ESF.x / self.convolution_point()
        return 0, 0, factor

    def NLO(self):
        self.init_nlo_vars()
        norm = 2.0 * constants.CF  # 2 = as_norm
        omx = norm * ic.f2_splus_soft(self)
        delta = norm * (ic.f2_splus_virt(self) + self.S)

        def reg(z):
            self.init_vars(z)
            return norm * (ic.f2_splus_raw(self) - ic.f2_splus_soft(self) / (1.0 - z))

        return rsl_from_distr_coeffs(reg, delta, omx)


class F2IntrinsicSm(PartonicChannelHeavyIntrinsic):
    def NLO(self):
        self.init_nlo_vars()
        norm = 2.0 * constants.CF  # 2 = as_norm
        omx = norm * ic.f2_sminus_soft(self)
        delta = norm * ic.f2_sminus_virt(self) + self.S

        def reg(z):
            self.init_vars(z)
            return norm * (ic.f2_sminus_raw(self) - ic.f2_sminus_soft(self) / (1.0 - z))

        return rsl_from_distr_coeffs(reg, delta, omx)
