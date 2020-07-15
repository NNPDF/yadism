# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`vogt` which includes also the lower order results.

.. todo::
    docs
"""

from .nc.f2_light import EvaluatedStructureFunctionF2light
from .nc.fl_light import EvaluatedStructureFunctionFLlight
from .nc.f_total import EvaluatedStructureFunctionFtotal
from .nc.f2_heavy import (
    EvaluatedStructureFunctionF2charm,
    EvaluatedStructureFunctionF2bottom,
    EvaluatedStructureFunctionF2top,
)
from .nc.fl_heavy import (
    EvaluatedStructureFunctionFLcharm,
    EvaluatedStructureFunctionFLbottom,
    EvaluatedStructureFunctionFLtop,
)
from .nc.f2_asymptotic import (
    EvaluatedStructureFunctionF2charmAsymptotic,
    EvaluatedStructureFunctionF2bottomAsymptotic,
    EvaluatedStructureFunctionF2topAsymptotic,
)
from .nc.fl_asymptotic import (
    EvaluatedStructureFunctionFLcharmAsymptotic,
    EvaluatedStructureFunctionFLbottomAsymptotic,
    EvaluatedStructureFunctionFLtopAsymptotic,
)

ESFmap = {
    # F2 -------
    "F2light": EvaluatedStructureFunctionF2light,
    "F2charm": EvaluatedStructureFunctionF2charm,
    "F2bottom": EvaluatedStructureFunctionF2bottom,
    "F2top": EvaluatedStructureFunctionF2top,
    "F2total": EvaluatedStructureFunctionFtotal,
    # asymptotics
    "F2charmasy": EvaluatedStructureFunctionF2charmAsymptotic,
    "F2bottomasy": EvaluatedStructureFunctionF2bottomAsymptotic,
    "F2topasy": EvaluatedStructureFunctionF2topAsymptotic,
    # FL -----
    "FLlight": EvaluatedStructureFunctionFLlight,
    "FLcharm": EvaluatedStructureFunctionFLcharm,
    "FLbottom": EvaluatedStructureFunctionFLbottom,
    "FLtop": EvaluatedStructureFunctionFLtop,
    "FLtotal": EvaluatedStructureFunctionFtotal,
    # asymptotics
    "FLcharmasy": EvaluatedStructureFunctionFLcharmAsymptotic,
    "FLbottomasy": EvaluatedStructureFunctionFLbottomAsymptotic,
    "FLtopasy": EvaluatedStructureFunctionFLtopAsymptotic,
}
