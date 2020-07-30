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
        # -Power(Pi,2)/6. + Li2(\[Lambda]) + Li2((-1 + \[Lambda])/(-1 + x*\[Lambda])) + ln(1 - \[Lambda])*ln(\[Lambda]) - ln(1 - x)*ln(1 - x*\[Lambda]) - ln(\[Lambda])*ln(1 - x*\[Lambda]) + Power(ln(1 - x*\[Lambda]),2)/2.
        pass


class F2heavyGluon(pc.PartonicChannel):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"
