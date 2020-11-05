# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
light quark flavours.

The coefficient functions definition is given in :eqref:`4.2`,
:cite:`vogt-f2nc` (that is the main reference for their expression, i.e. all
the formulas in this module).

Scale varitions main reference is :cite:`vogt-sv`.

"""

import numpy as np

from eko import constants

from .. import splitting_functions as split
from .. import partonic_channel as pc
from ..esf import rsl_from_distr_coeffs


class F2lightQuark(pc.PartonicChannelLight):
    """
        Computes the light quark channel of  F2light
    """

    label = "q"

    @staticmethod
    def LO():
        """
            Computes the quark singlet part of the leading order F2 structure function.

            This is the only contribution at all present in the LO, consisting
            in the simplest coefficient function possible (a delta, that makes
            the structure function completely proportional to the incoming PDF).

            |ref| implements :eqref:`4.2`, :cite:`vogt-f2nc`.

            Returns
            -------
                sequence of callables
                coefficient functions

        """

        # leading order is just a delta function
        return 0, 0, 1

    def NLO(self):
        """
            Computes the quark singlet part of the next to leading order F2
            structure function.

            |ref| implements :eqref:`4.3`, :cite:`vogt-f2nc`.

            Returns
            -------
                sequence of callables
                coefficient functions

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
            Computes the quark singlet contribution to the next to leading
            order F2 structure function coming from the factorization scheme.

            |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.

            Returns
            -------
                sequence of callables
                coefficient functions

            Note
            ----
                Check the theory reference for details on
                :doc:`../theory/scale-variations`

        """

        return split.pqq_reg, split.pqq_sing, split.pqq_local


class F2lightGluon(pc.PartonicChannelLight):
    """
        Computes the gluon channel of  F2light
    """

    label = "g"

    def NLO(self):
        """
            Computes the gluon part of the next to leading order F2 structure
            function.

            |ref| implements :eqref:`4.4`, :cite:`vogt-f2nc`.

            Returns
            -------
                sequence of callables
                    coefficient functions


            .. todo::
                - 2 * n_f here and in gluon_1_fact is coming from momentum sum
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
            Computes the gluon contribution to the next to leading order F2
            structure function coming from the factorization scheme.

            |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.

            Returns
            -------
                sequence of callables
                coefficient functions

            Note
            ----
                Check the theory reference for details on
                :doc:`../theory/scale-variations`

        """

        def cg(z, nf=self.nf):
            return 2.0 * nf * split.pqg(z)

        return cg
