# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightNonSinglet, F2lightGluon
from .fl_light import FLlightNonSinglet, FLlightGluon
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
        },
        "heavy": {
            "gVV": F2heavyGluonVV,
            "gAA": F2heavyGluonAA,
        },
        "asy": {
            "gVV": F2asyGluonVV,
        }
    },
    "FL": {
        "light": {
            "ns": FLlightNonSinglet,
            "g": FLlightGluon,
        },
        "heavy": {
            "gVV": FLheavyGluonVV,
            "gAA": FLheavyGluonAA,
        },
        "asy": {
            "gVV": FLasyGluonVV,
        }
    },
    "F3": {
        "light": {
            "ns": F3lightNonSinglet,
            "g": None,
        },
        "heavy": {
            "gVV": None,
            "gAA": None,
        },
        "asy": {
            "gVV": None,
        }
    }
}


# def weights_nc(obs_name, coupling_constants, Q2):
#     if obs_name.flavor == "light":
#         return weights_light(range(1, 3 + 1), coupling_constants, Q2, obs_name.kind)
#     elif obs_name.flavor_family == "light":
#         # so it's heavylight
#         return weights_light([obs_name.hqnumber], coupling_constants, Q2, obs_name.kind)
#     return weights_heavy(obs_name.hqnumber, coupling_constants, Q2, obs_name.kind)
