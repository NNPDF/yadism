import numba as nb
from yadism.esf import conv
from yadism.coefficient_functions.partonic_channel import RSL
from yadism.coefficient_functions.light.nlo.fl import gluon_reg
from eko.interpolation import InterpolatorDispatcher
import numpy as np

myid = InterpolatorDispatcher(np.array([0.1, 0.4, 0.7, 1.0]), 1, False, False)
gluon = RSL(reg=gluon_reg, sing=gluon_reg, args=np.array([3], dtype=float))


if __name__ == "__main__":
    print(conv.convolution(gluon, 0.5, myid[2]))
