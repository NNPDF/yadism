# -*- coding: utf-8 -*-

import copy

from .. import partonic_channel as pc

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


coefficient_functions = {
    "F2": {
        "light": {
            "q": F2lightQuark,
            "g": F2lightGluon,
        },
        "heavy": {
            "q": F2heavyQuark,
            "g": F2heavyGluon,
        },
        "asy": {
            "q": F2asyQuark,
            "g": F2asyGluon,
        }
    },
    "FL": {
        "light": {
            "q": FLasyQuark,
            "g": FLasyGluon,
        },
        "heavy": {
            "q": FLasyQuark,
            "g": FLasyGluon,
        },
        "asy": {
            "q": FLasyQuark,
            "g": FLasyGluon,
        }
    },
    "F3": {
        "light": {
            "q": F3lightQuark,
            "g": pc.EmptyPartonicChannel,
        },
        "heavy": {
            "q": F3heavyQuark,
            "g": F3heavyGluon,
        },
        "asy": {
            "q": F3asyQuark,
            "g": F3asyGluon,
        }
    }
}
