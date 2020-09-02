# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions

.. todo::
    docs
"""

from .. import partonic_channel as pc


class F2asyQuark(pc.PartonicChannelAsy):
    """
        Computes the quark channel of the asymptotic limit of F2heavy.
    """

    label = "q"

    def LO(self):
        return 0, 0, 1
