#!/usr/bin/python3
import numpy as np

import QCDNUM

QCDNUM.qcinit(6, "")

QCDNUM.setord(1)
QCDNUM.setalf(0.35, 2)

QCDNUM.gxmake([1e-5],[1],100,2)

QCDNUM.gqmake([5, 10],[1,1],11)

QCDNUM.extpdf(lambda *args:0, 1, 0, 0)
