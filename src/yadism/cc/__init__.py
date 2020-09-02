# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f3_light import F3lightQuark
from .f2_heavy import F2heavyQuark, F2heavyGluon
from .fl_heavy import FLheavyQuark, FLheavyGluon
from .f3_heavy import F3heavyQuark
from .f2_asy import F2asyQuark
from .fl_asy import FLasyQuark
from .f3_asy import F3asyQuark

from .weights import weight_factory

partonic_channels_cc = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F3light": [F3lightQuark],
    "F2heavy": [F2heavyQuark, F2heavyGluon],
    "FLheavy": [FLheavyQuark, FLheavyGluon],
    "F3heavy": [F3heavyQuark],
    "F2asy": [F2asyQuark],
    "FLasy": [FLasyQuark],
    "F3asy": [F3asyQuark],
}


def weights_cc(obs_name):
    if obs_name.flavor_family == "light":
        return weight_factory(obs_name.kind, "light")
    return weight_factory(obs_name.kind, obs_name.weight_family)


convolution_point_cc = {
    "light": lambda x, *args: x,
    "heavy": lambda x, Q2, m2hq: x * (1 + m2hq / Q2),
    "asy": lambda x, *args: x,
}
