# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""
import copy

import numpy as np

from .. import splitting_functions as split
from . import EvaluatedStructureFunctionAsymptoticNeutralCurrent as ESFasyNC

class EvaluatedStructureFunctionF2Asymptotic(ESFasyNC):
    """
        Compute F2 structure functions for heavy quark flavours.

        This class inherits from :py:class:`ESFH`, providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent (and, mainly, in its own parent).

        Even if this is still an intermediate class it has already enough
        information to be able to express coefficient functions, while children
        are used just ot handle differences among flavours (e.g. electric
        charge).

    """

    def gluon_1(self):
        """
            Returns
            -------
                sequence of callables
                    coefficient functions, as two arguments functions: :py:`(x, Q2)`

            .. todo::
                docs
        """
        TR = self._SF.constants.TF

        def cg(z,L=self.L, TR=TR):
            return 4. * (
                split.pqg(z, self._SF.constants) * (L + np.log((1-z)/z))
                + TR*( - 1 + 8*z*(1-z) )
            )

        return cg


class EvaluatedStructureFunctionF2charmAsymptotic(
    EvaluatedStructureFunctionF2Asymptotic
):
    """
        Compute F2 structure functions for *charm* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2Asymptotic`.
        Currently this class sets only:

        - nhq = 4

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2charmAsymptotic, self).__init__(
            SF, kinematics, nhq=4
        )


class EvaluatedStructureFunctionF2bottomAsymptotic(
    EvaluatedStructureFunctionF2Asymptotic
):
    """
        Compute F2 structure functions for *bottom* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2Asymptotic`.
        Currently this class sets only:

        - nhq = 5

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2bottomAsymptotic, self).__init__(
            SF, kinematics, nhq=5
        )


class EvaluatedStructureFunctionF2topAsymptotic(EvaluatedStructureFunctionF2Asymptotic):
    """
        Compute F2 structure functions for *top* quark.

        All the definitions and expression are already given at the level of
        :py:class:`EvaluatedStructureFunctionF2Asymptotic`.
        Currently this class sets only:

        - nhq = 6

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionF2topAsymptotic, self).__init__(
            SF, kinematics, nhq=6
        )
