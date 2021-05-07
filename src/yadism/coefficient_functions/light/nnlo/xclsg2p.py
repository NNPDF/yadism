# -*- coding: utf-8 -*-
# auto-generated module by light package
# pylint: skip-file
# fmt: off
import numpy as np


def cls2a(y, nf):
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    res = nf * ( (15.94 - 5.212 * y) * (1.-y)**2 * dl1 + (0.421 + 1.520 * y) * dl**2 + 28.09 * (1.-y) * dl - (2.370/y - 19.27) * (1.-y)**3 )
    return res
