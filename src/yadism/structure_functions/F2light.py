# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
light quark flavours (namely *up*, *bottom*, *strange*).

The only element present is the :py:class:`ESF_F2light`, that inherits the
:py:class:`EvaluatedStructureFunction` machinery, but it is used just to store
the definitions of the related coefficient functions formula.

The coefficient functions definition is given in :eqref:`4.2`, :cite:`vogt` (that
is the main reference for their expression, i.e. all the formulas in this
module).

Scale varitions main reference is :cite:`vogt-sv`.

"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split


class ESF_F2light(ESF):
    """
        Compute F2 structure functions for light quark flavours.

        This class inherits from :py:class:`ESF`, providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent.

    """

    def quark_0(self) -> float:
        """
            Computes the quark singlet part of the leading order F2 structure function.

            This is the only contribution at all present in the LO, consisting
            in the simplest coefficient function possible (a delta, that makes
            the structure function completely proportional to the incoming PDF).

            |ref| implements :eqref:`4.2`, :cite:`vogt`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

        """

        # leading order is just a delta function
        return lambda z: 0, lambda z: 1

    def quark_1(self):
        """
            Computes the quark singlet part of the next to leading order F2
            structure function.

            |ref| implements :eqref:`4.3`, :cite:`vogt`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

        """
        CF = self._SF.constants.CF
        zeta_2 = np.pi ** 2 / 6

        def cq_reg(z):
            # fmt: off
            return CF*(
                - 2 * (1 + z) * np.log((1 - z) / z)
                - 4 * np.log(z) / (1 - z)
                + 6 + 4 * z
            )
            # fmt: on

        def cq_delta(_z):
            return -CF * (9 + 4 * zeta_2)

        def cq_omx(_z):
            return -3 * CF

        def cq_logomx(_z):
            return 4 * CF

        return cq_reg, cq_delta, cq_omx, cq_logomx

    def quark_1_fact(self):
        """
            Computes the quark singlet contribution to the next to leading
            order F2 structure function coming from the factorization scheme.

            |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

            Note
            ----
            Check the theory reference for details on
            :doc:`../theory/scale-variations`

        """

        def cq_reg(z):
            return split.pqq_reg(z, self._SF.constants)

        def cq_delta(z):
            return split.pqq_delta(z, self._SF.constants)

        def cq_pd(z):
            return split.pqq_pd(z, self._SF.constants)

        return cq_reg, cq_delta, cq_pd

    def gluon_1(self):
        """
            Computes the gluon part of the next to leading order F2 structure
            function.

            |ref| implements :eqref:`4.4`, :cite:`vogt`.

            Returns
            -------
            sequence of callables
                coefficient functions, as two arguments functions: :py:`(x, Q2)`


            .. todo::
                - 2 * n_f here and in gluon_1_fact is coming from momentum sum
                  rule q_i -> {q_i, g} but g -> {g, q_i, \bar{q_i} forall i}, so
                  the 2 * n_f is needed to compensate for all the number of flavours
                  plus antiflavours in which the gluon can go.

        """

        TR = self._SF.constants.TF

        def cg(z):
            return (
                2  # TODO: to be understood
                * 2
                * self._n_f
                * (
                    split.pqg(z, self._SF.constants) * (np.log((1 - z) / z) - 4)
                    + 3 * TR
                )
            )

        return cg

    def gluon_1_fact(self):
        """
            Computes the gluon contribution to the next to leading order F2
            structure function coming from the factorization scheme.

            |ref| implements :eqref:`2.17`, :cite:`vogt-sv`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

            Note
            ----
            Check the theory reference for details on
            :doc:`../theory/scale-variations`

        """

        def cg(z):
            return 2 * self._n_f * split.pqg(z, self._SF.constants)

        return cg
