# -*- coding: utf-8 -*-

from . import f3_nc


class Rplus(f3_nc.Rplus):
    def __init__(self, ESF, m1sq):
        super().__init__(ESF, m1sq, 0.01)
