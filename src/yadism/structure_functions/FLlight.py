# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
light quark flavours (namely *up*, *bottom*, *strange*).

The only element present is the :py:class:`ESF_FLlight`, that inherits the
:py:class:`EvaluatedStructureFunction` machinery, but it is used just to store
the definitions of the related coefficient functions formula.

The main reference used is: :cite:`vogt`.

"""

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF


class ESF_FLlight(ESF):
    """
    .. todo::
        docs
    """

    def quark_0(self) -> float:
        """
        .. todo::
            docs
        """

        return 0

    def quark_1(self):
        """
        .. todo::
            docs
        """
        CF = self._SF.constants.CF

        def cq_reg(z):
            return CF * 4.0 * z

        return cq_reg

    def quark_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0

    def gluon_1(self):
        """
        vogt page 117

        .. todo::
            docs
        """

        def cg(z):
            return self._n_f * 8.0 * z * (1.0 - z)

        return cg

    def gluon_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0
