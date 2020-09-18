# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from .. import partonic_channel as pc


class F3asyQuarkVA(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "qVA"
