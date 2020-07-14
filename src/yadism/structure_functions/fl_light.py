# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
light quark flavours.

The only element present is the :py:class:`EvaluatedStructureFunctionFLlight`, that inherits the
:py:class:`EvaluatedStructureFunctionLight` machinery, but it is used just to store
the definitions of the related coefficient functions formula.

The coefficient functions definition is given in :eqref:`4.2`, :cite:`vogt` (the
same of :eqref:`1` in :cite:`vogt-fl`).
The main reference for their expression is :cite:`vogt-fl`.

Scale varitions main reference is :cite:`vogt-sv`.

"""

from .esf import EvaluatedStructureFunctionLight as ESFLight


class EvaluatedStructureFunctionFLlight(ESFLight):
    """
        Compute FL structure functions for light quark flavours.

        This class inherits from :py:class:`EvaluatedStructureFunctionLight`,
        providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent.

    """

    def quark_0(self) -> float:
        """
            Computes the quark singlet part of the leading order FL structure function.

            The LO is null because of Callan-Gross relation, cf. :cite:`vogt-fl`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

        """

        return 0

    def quark_1(self):
        """
            Computes the quark singlet part of the next to leading order FL
            structure function.

            |ref| implements :eqref:`3`, :cite:`vogt-fl`.

            Returns
            -------
            sequence of callables
               coefficient functions, as two arguments functions: :py:`(x, Q2)`

        """
        CF = self._SF.constants.CF

        def cq_reg(z):
            return CF * 4.0 * z

        return cq_reg

    def quark_1_fact(self):
        """
            Computes the quark singlet contribution to the next to leading
            order FL structure function coming from the factorization scheme.

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
        return 0

    def gluon_1(self):
        """
            Computes the gluon part of the next to leading order FL structure
            function.

            |ref| implements :eqref:`3`, :cite:`vogt-fl`.

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

        def cg(z):
            return self.nf * 8.0 * z * (1.0 - z)

        return cg

    def gluon_1_fact(self):
        """
            Computes the gluon contribution to the next to leading order FL
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
        return 0
