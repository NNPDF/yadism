# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions

.. todo::
    docs
"""

from .. import partonic_channel as pc


class FLasyQuark(pc.PartonicChannelAsy):
    """
        Computes the quark channel of the asymptotic limit of FLheavy.
    """

    label = "q"
