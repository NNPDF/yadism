# -*- coding: utf-8 -*-
from ..partonic_channel import RSL
from . import n3lo, nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """
        |ref| APFEL
        """

        # leading order is just a delta function
        return RSL.from_delta(1.0)

    @staticmethod
    def NLO():
        """
        |ref| APFEL
        """

        return RSL.from_distr_coeffs(
            nlo.g1.ns_reg, (nlo.g1.ns_delta, nlo.g1.ns_omx, nlo.g1.ns_logomx)
        )

    def NNLO(self):
        return None

class Gluon(pc.LightBase):
    def NLO(self):
        r"""
        |ref| APFEL

        Note
        ----
        2 * n_f is coming from momentum sum rule q_i -> {q_i, g} but
        g -> {g, q_i, \bar{q_i} forall i}, so the 2 * n_f is needed
        to compensate for all the number of flavours plus antiflavours
        in which the gluon can go.
        """

        return RSL(nlo.g1.gluon_reg, args=[self.nf])

    def NNLO(self):
        return None


class Singlet(pc.LightBase):
    def NNLO(self):
        return None

