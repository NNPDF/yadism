# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quarks
"""

# TODO

import numpy as np

from .. import partonic_channel as pc


class F2heavyQuark(pc.PartonicChannel):
    """
        Computes the quark heavy quark channel of F2heavy
    """

    label = "q"

    def LO(self):
        return 0, 0, 1

    def NLO(self):
        pass


class F2heavyGluon(pc.PartonicChannel):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"
