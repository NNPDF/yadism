# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`vogt` which includes also the lower order results.

.. todo::
    docs
"""

from .esf import EvaluatedStructureFunctionLight
from .esf import EvaluatedStructureFunctionHeavy

ESFmap = {
    # F2 -------
    # TODO key can be only flavor_family
    "F2light": EvaluatedStructureFunctionLight,
    "F2charm": EvaluatedStructureFunctionHeavy,
    # "F2bottom": None,
    # "F2top": None,
    # "F2total": None,
    # # asymptotics
    # "F2charmasy": None,
    # "F2bottomasy": None,
    # "F2topasy": None,
    # # FL -----
    "FLlight": EvaluatedStructureFunctionLight,
    # "FLlight": None,
    # "FLcharm": None,
    # "FLbottom": None,
    # "FLtop": None,
    # "FLtotal": None,
    # # asymptotics
    # "FLcharmasy": None,
    # "FLbottomasy": None,
    # "FLtopasy": None,
}
