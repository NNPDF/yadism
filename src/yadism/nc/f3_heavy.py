# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavors.

The main reference used is: :cite:`felix-thesis`.

"""

import numpy as np

from . import partonic_channel as pcnc


class F3heavyQuarkVA(pcnc.PartonicChannelHeavy):
    """
        Computes the gluon channel of F3heavy.

        :eqref:`D.7`
    """

    label = "qVA"
