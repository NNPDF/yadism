# -*- coding: utf-8 -*-
from .. import partonic_channel as pc
from ..partonic_channel import RSL
from . import f2_nc, nlo, nnlo


class NonSinglet(f2_nc.NonSinglet):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`155`, :cite:`moch-f3nc`.
        """

        return RSL.from_distr_coeffs(
            nlo.f3.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        return RSL(
            nnlo.xc3ns2p.c3np2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3np2c, [self.nf]
        )


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
