# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavors.

The main reference used is: :cite:`gluck-ccheavy`.

"""

import numpy as np

from . import partonic_channel as pccc


class F3heavyQuark(pccc.PartonicChannelHeavy):
    """
        Computes the gluon channel of F3heavy.

        :eqref:`D.7`
    """

    label = "q"

    def LO(self):
        return 0, 0, 1
