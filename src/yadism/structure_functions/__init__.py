# -*- coding: utf-8 -*-
"""
This subpackage contains the implementation of the DIS structure functions.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.
"""

from eko import t_float
from eko.interpolation import (
    evaluate_Lagrange_basis_function_x,
    evaluate_Lagrange_basis_function_log_x,
)
