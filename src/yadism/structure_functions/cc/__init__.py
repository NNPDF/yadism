# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon

from .weights import WeightLight

partonic_channels_cc = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
}


weigths_cc = {
    "light": WeightLight,
}