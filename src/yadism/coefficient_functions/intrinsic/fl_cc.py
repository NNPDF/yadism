# -*- coding: utf-8 -*-

from . import fl_nc


class Splus(fl_nc.Splus):
    def __init__(self, ESF, m1sq):
        super().__init__(ESF, m1sq, 0.01)
