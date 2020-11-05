# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f3_light import F3lightQuark
from .f2_heavy import F2heavyQuark, F2heavyGluon
from .fl_heavy import FLheavyQuark, FLheavyGluon
from .f3_heavy import F3heavyQuark, F3heavyGluon
from .f2_asy import F2asyQuark, F2asyGluon
from .fl_asy import FLasyQuark, FLasyGluon
from .f3_asy import F3asyQuark, F3asyGluon

from .weights import weights as weights_cc

partonic_channels_cc = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F3light": [F3lightQuark],
    "F2heavy": [F2heavyQuark, F2heavyGluon],
    "FLheavy": [FLheavyQuark, FLheavyGluon],
    "F3heavy": [F3heavyQuark, F3heavyGluon],
    "F2asy": [F2asyQuark, F2asyGluon],
    "FLasy": [FLasyQuark, FLasyGluon],
    "F3asy": [F3asyQuark, F3asyGluon],
}


convolution_point_cc = {
    "light": lambda x, *args: x,
    "heavy": lambda x, Q2, m2hq: x * (1 + m2hq / Q2),
    "asy": lambda x, *args: x,
}
