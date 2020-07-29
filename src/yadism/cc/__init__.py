# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f2_heavy import F2heavyQuark, F2heavyGluon

from .weights import weight_factory

partonic_channels_cc = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F2heavy": [F2heavyQuark, F2heavyGluon],
}


weigths_cc = {
    "light": weight_factory("light"),
    "charm": weight_factory("charm"),
    "charmlight": weight_factory("light"),
    "bottom": weight_factory("bottom"),
    "bottomlight": weight_factory("light"),
    "top": weight_factory("top"),
    "toplight": weight_factory("light"),
}

convolution_point_cc = {
    "light": lambda x, *args: x,
    "heavy": lambda x, Q2, m2hq: x * (1 + m2hq / Q2),
    "asy": lambda x, *args: x,
}
