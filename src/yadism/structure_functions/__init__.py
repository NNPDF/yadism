# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`vogt` which includes also the lower order results.

.. todo::
    docs
"""

from .f2_light import EvaluatedStructureFunctionF2light
from .fl_light import EvaluatedStructureFunctionFLlight
from .f_total import EvaluatedStructureFunctionFtotal
from .f2_heavy import (
    EvaluatedStructureFunctionF2charm,
    EvaluatedStructureFunctionF2bottom,
    EvaluatedStructureFunctionF2top,
)
from .fl_heavy import (
    EvaluatedStructureFunctionFLcharm,
    EvaluatedStructureFunctionFLbottom,
    EvaluatedStructureFunctionFLtop,
)

ESFmap = {
    "F2light": EvaluatedStructureFunctionF2light,
    "F2charm": EvaluatedStructureFunctionF2charm,
    "F2bottom": EvaluatedStructureFunctionF2bottom,
    "F2top": EvaluatedStructureFunctionF2top,
    "FLlight": EvaluatedStructureFunctionFLlight,
    "FLcharm": EvaluatedStructureFunctionFLcharm,
    "FLbottom": EvaluatedStructureFunctionFLbottom,
    "FLtop": EvaluatedStructureFunctionFLtop,
    "F2total": EvaluatedStructureFunctionFtotal,
    "FLtotal": EvaluatedStructureFunctionFtotal,
}
