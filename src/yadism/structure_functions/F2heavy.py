# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split


class ESF_F2heavy(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        super(ESF_F2light, self).__init__(SF, kinematics)

    def quark_0(self) -> float:
        return 0

    def gluon_0(self) -> float:
        return 0

    def quark_1(self):
        """
        regular
        delta
        1/(1-x)_+
        log(x)/(1-x)_+

        .. todo::
            docs
        """
        return 0

    def gluon_1(self):
        """
        vogt page 21

        .. todo::
            docs
        """

        TR = self._SF._constants.TF

        def cg(z):
            return (
                2
                * self._n_f
                * (
                    split.pqg(z, self._SF._constants) * (np.log((1 - z) / z) - 4)
                    + 3 * TR
                )
            )

        return cg
