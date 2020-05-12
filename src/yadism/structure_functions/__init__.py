# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.

.. todo::
    docs
"""

from .F2light import ESF_F2light
from .FLlight import ESF_FLlight
from .F2heavy import ESF_F2charm, ESF_F2bottom, ESF_F2top
from .FLheavy import ESF_FLcharm, ESF_FLbottom, ESF_FLtop

ESFmap = {
    "F2light": ESF_F2light,
    "F2charm": ESF_F2charm,
    "F2bottom": ESF_F2bottom,
    "F2top": ESF_F2top,
    "FLlight": ESF_FLlight,
    "FLcharm": ESF_FLcharm,
    "FLbottom": ESF_FLbottom,
    "FLtop": ESF_FLtop,
}
