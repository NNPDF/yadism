# -*- coding: utf-8 -*-
r"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavors.

The main reference used is: :cite:`gluck-ccheavy`.

.. todo:: write about FL=F2-2xF1 and all the normalization business

"""

import numpy as np

from . import partonic_channel as pccc
from .. import splitting_functions as split


class F3heavyQuark(pccc.PartonicChannelHeavy):
    """
        Computes the light quark channel of F3heavy.

        :eqref:`2` of :cite:`gluck-ccheavy`
    """

    label = "q"

    def LO(self):
        return 0, 0, self.labda


class F3heavyGluon(pccc.PartonicChannelHeavy):
    """
        Computes the gluon channel of F3heavy

        :eqref:`A5` of :cite:`gluck-ccheavy`
    """

    label = "g"

    def NLO(self):
        def reg(z):
            c1 = 2.0 * (1.0 - self.labda)
            c2 = 0
            c3 = -2.0 * (1.0 - z)
            c4 = 2
            return (
                (
                    (
                        split.pqg(z, self.constants)
                        * (-self.l_labda(z) - np.log(self.labda))
                    )
                    + self.h_g(z, [c1, c2, c3, c4])
                )
                * self.labda
                * 2
            )

        return reg
