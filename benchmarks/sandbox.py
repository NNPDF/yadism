# -*- coding: utf-8 -*-
# pylint: skip-file
# Compare the results with APFEL's
import copy

import numpy as np

from yadmark.db_interface import (  # pylint: disable=unused-import
    DBInterface,
    QueryFieldsEqual,
)

from yadmark.data import observables


def generate_observables():
    og = observables.ObservablesGenerator("sandbox")
    defaults = og.get_observables()[0]
    #xgrid = np.array(defaults["interpolation_xgrid"]).copy()
    #defaults["interpolation_xgrid"] = np.unique(np.concatenate([xgrid, (1. + 4./90.)*xgrid[:-1]]))
    light_kin = []
    light_kin.extend(
        [dict(x=x, Q2=90.0) for x in defaults["interpolation_xgrid"][::3]]
        # np.linspace(1e-3, 1, 50)
    )
    light_kin.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
    obs_list = [
        "F2light",
        "F2charm",
        "F2bottom",
        "F2top",
        "FLlight",
        "FLcharm",
        "FLbottom",
        "FLtop",
    ]
    cards = []
    # for obs in ["F2charm"]:  # obs_list:
    for obs in ["FLcharm"]:  # obs_list:
        card = copy.deepcopy(defaults)
        #card["interpolation_xgrid"] = list(card["interpolation_xgrid"])
        #print(card)
        card["prDIS"] = "CC"
        # card["PropagatorCorrection"] = .999
        card["ProjectileDIS"] = "neutrino"
        # card["PolarizationDIS"] = 1.0
        card[obs] = light_kin
        cards.append(card)
    og.write_observables(cards)


class ApfelSandbox:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self):
        """init DB connection"""
        self.db = DBInterface("sandbox", "APFEL")
        return self.db

    def run_LO(self):
        return self._db().run_external(0, ["gonly"])

    def run_NLO(self):
        return self._db().run_external(
            1,
            ["gonly"],
            # {
            # "FNS": self.db.theory_query.FNS == "FONLL-A",
            # "DAMP": self.db.theory_query.DAMP == 0,
            # },
        )


if __name__ == "__main__":
    generate_observables()
    apf = ApfelSandbox()
    #apf.run_LO()
    apf.run_NLO()
