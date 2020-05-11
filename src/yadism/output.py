# -*- coding: utf-8 -*-
"""
Output
------

.. todo::
    docs
"""

import numpy as np


class Output(dict):
    """
        .. todo::
            docs
    """

    # TODO shift function somewhere else?
    # the other alternative is to shift this to an external module (and ouf of runner)
    # and import from there, here and in yadism.__init__
    def apply_PDF(self, pdfs):
        # iterate
        ret: dict = {}
        for obs in self:
            if obs[0] != "F":
                continue
            if self[obs] is None:
                continue
            ret[obs] = []
            for kin in self[obs]:
                ret[obs].append(kin.apply_PDF(self["xgrid"], self["xiF"], pdfs))
        return ret

    def dump(self):
        pass
