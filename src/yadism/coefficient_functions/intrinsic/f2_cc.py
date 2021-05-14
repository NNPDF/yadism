# -*- coding: utf-8 -*-

import numpy as np

from eko import constants

from .. import partonic_channel as pc
from ..partonic_channel import RSL

from . import raw_cc

from . import f2_nc


class Splus(f2_nc.Splus):
    def __init__(self, ESF, m1sq):
        super().__init__(ESF, m1sq, 0.01)


# class Splus(pc.PartonicChannel):
#     """
#     The convolution point simplifies to :math:`x` when m2=0,
#     see :eqref:`6` of :cite:`kretzer-schienbein`.
#     """
#     def __init__(self, ESF, m1sq):
#         super().__init__(ESF)
#         self.m1sq = m1sq
#         self.y = -ESF.Q2 / m1sq
#         self.lo = (1.-1./self.y)

#     def LO(self):
#         return RSL.from_delta(self.lo)

#     def NLO(self):
#         norm = self.lo * constants.CF
#         lnomx = raw_cc.lnomx * norm
#         omx = raw_cc.omx(self.y) * norm
#         delta = raw_cc.f2sv(self.y) * norm
#         def reg(z, args):
#             return (norm * raw_cc.f2r(self.y,z) - (lnomx*np.log(1.-z) + omx)/(1.-z))
#         return RSL.from_distr_coeffs(reg, (delta, omx, lnomx))
