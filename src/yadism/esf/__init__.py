# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

.. todo::
    docs
"""

import numpy as np

from .esf import (
    EvaluatedStructureFunction,
)

ESFmap = {
    "light": EvaluatedStructureFunction,
    "heavy": EvaluatedStructureFunction,
    "asy": EvaluatedStructureFunction,
    "total": EvaluatedStructureFunction,
}
