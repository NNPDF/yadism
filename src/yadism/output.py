# -*- coding: utf-8 -*-
"""
Output
------

.. todo::
    docs
"""

from .esf.esf_result import ESFResult


class Output(dict):
    """
        .. todo::
            docs
    """

    def apply_pdf(self, pdfs):
        # iterate
        ret: dict = {}
        for obs in self:
            if obs[0] != "F":
                continue
            if self[obs] is None:
                continue
            ret[obs] = []
            for kin in self[obs]:
                ret[obs].append(
                    ESFResult.from_dict(kin).apply_pdf(self["xgrid"], self["xiF"], pdfs)
                )
        return ret

    def dump(self):
        pass

    def load(self):
        pass
