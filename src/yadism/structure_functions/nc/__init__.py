# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f2_asy import F2asyGluonVV, F2asyGluonAA
from .fl_asy import FLasyGluonVV, FLasyGluonAA

partonic_channels_em = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F2heavy": [F2heavyGluonVV],
    "FLheavy": [FLheavyGluonVV],
    "F2asy": [F2asyGluonVV],
    "FLasy": [FLasyGluonVV],
}

# in NC for HQ new channels open: gluon_aa
partonic_channels_nc = copy.deepcopy(partonic_channels_em)
partonic_channels_nc["F2heavy"].extend([F2heavyGluonAA])
partonic_channels_nc["FLheavy"].extend([FLheavyGluonAA])
partonic_channels_nc["F2asy"].extend([F2asyGluonAA])
partonic_channels_nc["FLasy"].extend([FLasyGluonAA])
