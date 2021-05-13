# -*- coding: utf-8 -*-
import numpy as np

from eko import constants

from . import partonic_channel as pc

from .. import splitting_functions as split
from ...esf.distribution_vec import rsl_from_distr_coeffs

from . import nnlo


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """
        |ref| implements :eqref:`4.2`, :cite:`vogt-f2nc`.
        """

        # leading order is just a delta function
        return 0.0, 0.0, 1.0

    def NLO(self):
        """
        |ref| implements :eqref:`4.3`, :cite:`vogt-f2nc`.
        """
        CF = constants.CF
        zeta_2 = np.pi ** 2 / 6.0

        def reg(z, CF=CF):
            # fmt: off
            return CF*(
                - 2 * (1 + z) * np.log((1 - z) / z)
                - 4 * np.log(z) / (1 - z)
                + 6 + 4 * z
            )
            # fmt: on

        delta = -CF * (9 + 4 * zeta_2)

        omx = -3 * CF

        logomx = 4 * CF

        return rsl_from_distr_coeffs(reg, delta, omx, logomx)

    def NLO_fact(self):
        """
        |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.
        """

        return split.pqq_reg, split.pqq_sing, split.pqq_local

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        def reg(z):
            return nnlo.xc2ns2p.c2nn2a(z, self.nf)

        def sing(z):
            return nnlo.xc2ns2p.c2ns2b(z, self.nf)

        def loc(x):
            return nnlo.xc2ns2p.c2nn2c(x, self.nf)

        return reg, sing, loc


class Gluon(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`4.4`, :cite:`vogt-f2nc`.

        Note
        ----
        2 * n_f here and in NLO_fact is coming from momentum sum
        rule q_i -> {q_i, g} but g -> {g, q_i, \bar{q_i} forall i}, so
        the 2 * n_f is needed to compensate for all the number of flavours
        plus antiflavours in which the gluon can go.
        """

        def reg(z, nf=self.nf):
            return (
                nf
                * (
                    (2.0 - 4.0 * z * (1.0 - z)) * np.log((1.0 - z) / z)
                    - 2.0
                    + 16.0 * z * (1.0 - z)
                )
                * (2.0 * constants.TR)
            )

        return reg

    def NLO_fact(self):
        """
        |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.
        """

        def reg(z, nf=self.nf):
            return 2.0 * nf * split.pqg(z)

        return reg

    def NNLO(self):
        """
        |ref| implements :eqref:`4.10`, :cite:`vogt-f2nc`.
        """

        def reg(z):
            return nnlo.xc2sg2p.c2g2a(z, self.nf)

        def loc(x):
            return nnlo.xc2sg2p.c2g2c(x, self.nf)

        return reg, 0.0, loc


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`4.9`, :cite:`vogt-f2nc`.
        """

        def reg(z):
            return nnlo.xc2sg2p.c2s2a(z, self.nf)

        return reg, 0.0, 0.0
