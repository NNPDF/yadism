# -*- coding: utf-8 -*-
import numpy as np

from . import f2_nc
from .. import partonic_channel as pc
from ...esf.distribution_vec import rsl_from_distr_coeffs

from . import nlo
from . import nnlo


class NonSinglet(f2_nc.NonSinglet):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`155`, :cite:`moch-f3nc`.
        """

        def reg(z):
            return nlo.f3.ns_reg(z, np.array([], dtype=float))

        return rsl_from_distr_coeffs(
            reg, nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx
        )

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        def reg(z):
            return nnlo.xc3ns2p.c3np2a(z, np.array([self.nf], dtype=float))

        def sing(z):
            return nnlo.xc3ns2p.c3ns2b(z, np.array([self.nf], dtype=float))

        def loc(x):
            return nnlo.xc3ns2p.c3np2c(x, np.array([self.nf], dtype=float))

        return reg, sing, loc


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
