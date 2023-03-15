from ..partonic_channel import RSL
from . import nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """
        |ref| implements LO-part of :eqref:`A.1`, :cite:`Zijlstra-light-nnlo-pol`.
        """

        # leading order is just a delta function
        return RSL.from_delta(1.0)

    @staticmethod
    def NLO():
        """
        |ref| implements the equivalence relation between :math:`g_1` and :math:`F_3`
        as explained in :eqref:`A.19` (and paragraph below) of :cite:`Borsa-light-nnlo-pol`.
        For the explicit expressions, refer to :eqref:`A.1` of :cite:`Zijlstra-light-nnlo-pol`
        and :eqref:`15` of :cite:`deFlorian-light-nlo-pol`.
        """

        return RSL.from_distr_coeffs(
            nlo.g1.ns_reg, (nlo.g1.ns_delta, nlo.g1.ns_omx, nlo.g1.ns_logomx)
        )

    def NNLO(self):
        """
        |ref| implements the equivalence relation between :math:`g_1` and :math:`F_3`
        as explained in :eqref:`A.19` (and paragraph below) of :cite:`Borsa-light-nnlo-pol`.
        For the explicit expressions, refer to :eqref:`A.1` of :cite:`Zijlstra-light-nnlo-pol`
        and :eqref:`15` of :cite:`deFlorian-light-nlo-pol`.
        """

        return RSL(
            nnlo.xc3ns2p.c3np2a, nnlo.xc3ns2p.c3ns2b, nnlo.xc3ns2p.c3np2c, [self.nf]
        )


class Gluon(pc.LightBase):
    def NLO(self):
        r"""
        |ref| implements NLO-part of :eqref:`A.5`, :cite:`Zijlstra-light-nnlo-pol`.
        For a simpler expression, refer also to :eqref:`9` of :cite:`deFlorian-light-nlo-pol`.

        Note
        ----
        2 * n_f is coming from momentum sum rule q_i -> {q_i, g} but
        g -> {g, q_i, \bar{q_i} forall i}, so the 2 * n_f is needed
        to compensate for all the number of flavours plus antiflavours
        in which the gluon can go.
        """

        return RSL(nlo.g1.gluon_reg, args=[self.nf])

    def NNLO(self):
        """
        |ref| implements |NNLO| massless contribution of :eqref:`A.5`, :cite:`Zijlstra-light-nnlo-pol`.

        Note
        ----
        The actual implementation is taken from Apfel++ :cite:`Bertone:2017gds`:, see also:

            https://github.com/vbertone/apfelxx/blob/master/src/structurefunctions/zeromasscoefficientfunctionspol_sl.cc

        """
        return RSL(nnlo.g1.gluon_reg, args=[self.nf])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements |NNLO| massless contribution of :eqref:`A.4`, :cite:`Zijlstra-light-nnlo-pol`.

        Note
        ----
        The actual implementation is taken from Apfel++ :cite:`Bertone:2017gds`:, see also:

            https://github.com/vbertone/apfelxx/blob/master/src/structurefunctions/zeromasscoefficientfunctionspol_sl.cc

        """
        return RSL(nnlo.g1.singlet_reg, args=[self.nf])
