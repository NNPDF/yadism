# -*- coding: utf-8 -*-

import copy

from .. import partonic_channel as pc

from .f2_light import F2lightNonSinglet, F2lightGluon, F2lightSinglet
from .fl_light import FLlightNonSinglet, FLlightGluon, FLlightSinglet
from .f3_light import F3lightNonSinglet
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f2_asy import F2asyGluonVV, F2asyGluonAA
from .fl_asy import FLasyGluonVV, FLasyGluonAA

from .weights import weights_light, weights_heavy

coefficient_functions = {
    "F2": {
        "light": {
            "ns": F2lightNonSinglet,
            "g": F2lightGluon,
            "s": F2lightSinglet,
        },
        "heavy": {
            "gVV": F2heavyGluonVV,
            "gAA": F2heavyGluonAA,
        },
        "asy": {
            "gVV": F2asyGluonVV,
        },
    },
    "FL": {
        "light": {
            "ns": FLlightNonSinglet,
            "g": FLlightGluon,
            "s": FLlightSinglet,
        },
        "heavy": {
            "gVV": FLheavyGluonVV,
            "gAA": FLheavyGluonAA,
        },
        "asy": {
            "gVV": FLasyGluonVV,
        },
    },
    "F3": {
        "light": {
            "ns": F3lightNonSinglet,
            "g": pc.EmptyPartonicChannel,
            "s": pc.EmptyPartonicChannel,
        },
        "heavy": {
            "gVV": pc.EmptyPartonicChannel,
            "gAA": pc.EmptyPartonicChannel,
        },
        "asy": {
            "gVV": pc.EmptyPartonicChannel,
        },
    },
}
