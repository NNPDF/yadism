from ..partonic_channel import RSL
from . import nlo
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
        |ref| implements NLO-part of :eqref:`A.1`, :cite:`Zijlstra-light-nnlo-pol`.
        For a simpler expression, refer also to :eqref:`15` of :cite:`deFlorian-light-nlo-pol`.
        """

        return RSL.from_distr_coeffs(
            nlo.g1.ns_reg, (nlo.g1.ns_delta, nlo.g1.ns_omx, nlo.g1.ns_logomx)
        )

    def NNLO(self):
        return None


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
        return None


class Singlet(pc.LightBase):
    def NNLO(self):
        return None
