# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f2_heavy import F2heavyGluon

partonic_channels_em = {
    "F2light":  [F2lightQuark, F2lightGluon],
    "FLlight":  [FLlightQuark, FLlightGluon],
    "F2heavy":  [F2heavyGluon],
}

# in NC for HQ new channels open: gluon_aa
partonic_channels_nc = copy.deepcopy(partonic_channels_em)
#partonic_channels_nc["F2heavy"].extend([])
