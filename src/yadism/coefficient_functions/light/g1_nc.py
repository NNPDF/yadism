import numpy as np
from eko.constants import CF, TR

from ..partonic_channel import RSL
from ..special import li2, zeta2
from ..special.nielsen import nielsen
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
        |ref| implements the equivalence relation between :math:`g_1` and :math:`F_3`
        as explained in :eqref:`A.19` (and paragraph below). For the explicit expressions,
        refer to :eqref:`A.1` of :cite:`Zijlstra-light-nnlo-pol` and :eqref:`15` of
        :cite:`deFlorian-light-nlo-pol`.
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
        """
        |ref| implements |NNLO| massless contribution of :eqref:`A.4`, :cite:`Zijlstra-light-nnlo-pol`.

        """

        def singlet_reg(z, nf):
            ln = np.log(z)
            lnm1 = np.log(1 - z)
            li2m1 = li2(1 - z)
            li3m1 = nielsen(2, 1, 1 - z)
            res_lm0 = (1 + z) * (
                -16 * li3m1
                + 16 * lnm1 * li2m1
                - 16 * ln * li2m1
                - 16 * zeta2 * ln
                + 8 * ln * lnm1**2
                - 16 * ln**2 * lnm1
                + 20 / 3 * ln**3
            )
            +(1 - z) * (20 * lnm1**2 - 88 * lnm1 + 808 / 3) - 32 * (
                1 + 1 / 3 * z**2 + z + 1 / (3 * z)
            ) * (li2(-z) + ln * np.log(1 + z))
            (
                +(58 + 16 / 3 * z**2 - 6 * z) * ln**2
                - 32 * (2 - z) * ln * lnm1
                + 4 / 3 * (137 - 19 * z) * ln
                - (72 + 32 / 3 * z**2 - 40 * z) * zeta2
            )
            return nf * CF * TR * (res_lm0)

        return RSL(singlet_reg, args=[self.nf])
