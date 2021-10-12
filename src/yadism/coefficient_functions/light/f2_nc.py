# -*- coding: utf-8 -*-
from ..partonic_channel import RSL
from . import nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """
        |ref| implements :eqref:`4.2`, :cite:`vogt-f2nc`.
        """

        # leading order is just a delta function
        return RSL.from_delta(1.0)

    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`4.3`, :cite:`vogt-f2nc`.
        """

        return RSL.from_distr_coeffs(
            nlo.f2.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        return RSL(
            nnlo.xc2ns2p.c2nn2a, nnlo.xc2ns2p.c2ns2b, nnlo.xc2ns2p.c2nn2c, [self.nf]
        )


class Gluon(pc.LightBase):
    def NLO(self):
        r"""
        |ref| implements :eqref:`4.4`, :cite:`vogt-f2nc`.

        Note
        ----
        2 * n_f is coming from momentum sum
        rule q_i -> {q_i, g} but g -> {g, q_i, \bar{q_i} forall i}, so
        the 2 * n_f is needed to compensate for all the number of flavours
        plus antiflavours in which the gluon can go.
        """

        return RSL(nlo.f2.gluon_reg, args=[self.nf])

    def NNLO(self):
        """
        |ref| implements :eqref:`4.10`, :cite:`vogt-f2nc`.
        """

        return RSL(nnlo.xc2sg2p.c2g2a, loc=nnlo.xc2sg2p.c2g2c, args=[self.nf])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`4.9`, :cite:`vogt-f2nc`.
        """

        return RSL(nnlo.xc2sg2p.c2s2a, args=[self.nf])
