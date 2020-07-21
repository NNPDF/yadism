# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f2_asy import F2asyGluon
from .fl_asy import FLasyGluon

partonic_channels_em = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F2heavy": [F2heavyGluonVV],
    "FLheavy": [FLheavyGluonVV],
    "F2asy": [F2asyGluon],
    "FLasy": [FLasyGluon],
}

# in NC for HQ new channels open: gluon_aa
partonic_channels_nc = copy.deepcopy(partonic_channels_em)
partonic_channels_nc["F2heavy"].extend([F2heavyGluonAA])
partonic_channels_nc["FLheavy"].extend([FLheavyGluonAA])
