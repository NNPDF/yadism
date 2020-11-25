# -*- coding: utf-8 -*-
import copy
from numbers import Number


class Kernel:
    def __init__(self, partons, coeff):
        self.partons = partons
        self.coeff = coeff

    def __neg__(self):
        return self.__rmul__(-1)

    def __mul__(self, f):
        return self.__rmul__(f)

    def __rmul__(self, f):
        if not isinstance(f, Number):
            raise ValueError("Can only multiply numbers")
        partons = {k: f * v for k, v in self.partons.items()}
        return self.__class__(partons, copy.copy(self.coeff))
