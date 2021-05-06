# -*- coding: utf-8 -*-
# fmt: off
import numpy as np


def clnn2a (y, nf):
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    return (- 40.41 + 97.48 * y+ (26.56 * y - 0.031) * dl**2 - 14.85 * dl+ 13.62 * dl1**2 - 55.79 * dl1 - 150.5 * dl * dl1+ nf * 16./27.e0 * ( 6.* y*dl1 - 12.* y*dl - 25.* y + 6.))

def clnc2a (y, nf):
    dl  = np.log(y)
    dl1 = np.log(1.-y)
    return (- 52.27 + 100.8 * y+ (23.29 * y - 0.043) * dl**2 - 22.21 * dl+ 13.30 * dl1**2 - 59.12 * dl1 - 141.7 * dl * dl1+ nf * 16./27.e0 * ( 6.* y*dl1 - 12.* y*dl - 25.* y + 6.))

def clnn2c (y):
    return ( -0.164)

def clnc2c (y):
    return ( -0.150)