# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`vogt` which includes also the lower order results.

.. todo::
    docs
"""

from .esf.esf import (
    EvaluatedStructureFunction,
    EvaluatedStructureFunctionLight,
    EvaluatedStructureFunctionHeavy,
)
from .f_total import EvaluatedStructureFunctionFtotal

ESFmap = {
    "light": EvaluatedStructureFunctionLight,
    "heavy": EvaluatedStructureFunctionHeavy,
    "asy": EvaluatedStructureFunction,
    "total": EvaluatedStructureFunctionFtotal,
}
