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
        def get_charged_sum(z: float, Q2: float) -> float:
            """Short summary.

            d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9

            .. todo::
                docs
            """
            pdf_fl = lambda k: pdfs.xfxQ2(k, z, Q2)
            return (pdf_fl(1) + pdf_fl(-1) + pdf_fl(3) + pdf_fl(-3)) / 9 + (
                pdf_fl(2) + pdf_fl(-2)
            ) * 4 / 9

        ret: dict = {}
        for obs in self:
            if obs[0] != "F":
                continue
            if self[obs] is None:
                continue
            ret[obs] = []
            for kin in self[obs]:
                # collect pdfs
                fq = []
                fg = []
                for z in self["xgrid"]:
                    fq.append(get_charged_sum(z, kin["Q2"] * self["xiF"] ** 2) / z)
                    fg.append(pdfs.xfxQ2(21, z, kin["Q2"] * self["xiF"] ** 2) / z)

                # contract with coefficient functions
                result = kin["x"] * (
                    np.dot(fq, kin["q"]) + 2 / 9 * np.dot(fg, kin["g"])
                )
                error = kin["x"] * (
                    np.dot(fq, kin["q_error"]) + 2 / 9 * np.dot(fg, kin["g_error"])
                )
                ret[obs].append(
                    dict(x=kin["x"], Q2=kin["Q2"], result=result, error=error)
                )

        return ret
