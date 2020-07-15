# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""
import copy

from ..esf import EvaluatedStructureFunctionHeavy as ESFH


class EvaluatedStructureFunctionFLAsymptotic(ESFH):
    """
        Compute FL structure functions for heavy quark flavours.

        This class inherits from :py:class:`EvaluatedStructureFunctionHeavy`,
        providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent (and, mainly, in its own parent).

        Even if this is still an intermediate class it has already enough
        information to be able to express coefficient functions, while children
        are used just ot handle differences among flavours (e.g. electric
        charge).

    """

    def get_result(self):
        """
            .. todo::
                docs
        """
        self._compute_local()

        return copy.deepcopy(self._res)

    def _gluon_1(self):
        """
            Returns
            -------
                sequence of callables
                    coefficient functions, as two arguments functions: :py:`(x, Q2)`

            .. todo::
                docs
        """
        TF = self._SF.constants.TF

        def cg(z):
            if self.is_below_threshold(z):
                return 0
            return TF * (16 * z * (1 - z))  # self._FHprefactor

        return cg


class EvaluatedStructureFunctionFLcharmAsymptotic(
    EvaluatedStructureFunctionFLAsymptotic
):
    """
        Compute FL structure functions for *charm* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionFLAsymptotic`.
        Currently this class sets only:

        - nhq = 4

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLcharmAsymptotic, self).__init__(
            SF, kinematics, nhq=4
        )


class EvaluatedStructureFunctionFLbottomAsymptotic(
    EvaluatedStructureFunctionFLAsymptotic
):
    """
        Compute FL structure functions for *bottom* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionFLAsymptotic`.
        Currently this class sets only:

        - nhq = 5

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLbottomAsymptotic, self).__init__(
            SF, kinematics, nhq=5
        )


class EvaluatedStructureFunctionFLtopAsymptotic(EvaluatedStructureFunctionFLAsymptotic):
    """
        Compute FL structure functions for *top* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionFLAsymptotic`.
        Currently this class sets only:

        - nhq = 6

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLtopAsymptotic, self).__init__(
            SF, kinematics, nhq=6
        )
