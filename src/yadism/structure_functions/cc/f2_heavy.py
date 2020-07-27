# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quarks
"""

# TODO

import numpy as np

from .. import partonic_channel as pc


class F2heavyQuark(pc.PartonicChannelHeavy):
    """
        Computes the quark heavy quark channel of F2heavy
    """

    label = "q"

    def LO(self):



class F2heavyGluon(pc.PartonicChannelHeavy):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"
