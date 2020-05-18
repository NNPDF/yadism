# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
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
