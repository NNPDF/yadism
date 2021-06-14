# -*- coding: utf-8 -*-
# pylint: skip-file

import copy

import numpy as np

from banana.data import cartesian_product, theories
from yadmark.data import observables, pineappl_xgrid

import yadism


class Pineappl:

    obs_name = "F2_light"

    def generate_observables(self):
        defaults = copy.deepcopy(observables.default_card)
        defaults["interpolation_xgrid"] = pineappl_xgrid
        defaults["interpolation_polynomial_degree"] = 3
        xgrid = np.array(defaults["interpolation_xgrid"]).copy()
        # interpolation_xgrid = np.linspace(1e-1, 1, 9).tolist()
        kinematics = []
        kinematics.extend(
            [dict(x=x, Q2=20.0, y=0) for x in np.geomspace(1e-4, 0.9, 10)]
        )
        kinematics.extend(
            [dict(x=x, Q2=1.51 ** 2, y=0) for x in np.geomspace(1e-4, 0.9, 10)]
        )
        kinematics.extend(
            [dict(x=0.1, Q2=Q2, y=0) for Q2 in np.geomspace(4, 20, 10).tolist()]
        )
        kinematics.extend(
            [dict(x=0.001, Q2=Q2, y=0) for Q2 in np.geomspace(4, 20, 10).tolist()]
        )
        observable_names = [self.obs_name]
        # update = {"prDIS": ["EM"],"interpolation_xgrid":[interpolation_xgrid], "interpolation_polynomial_degree": [4]}
        update = {"prDIS": ["NC"], "ProjectileDIS": ["electron"]}
        obs = []
        for el in observables.build(
            observable_names=observable_names, kinematics=kinematics, update=update
        ):
            ocard = copy.deepcopy(defaults)
            ocard.update(el)
            obs.append(ocard)
        return obs

    @staticmethod
    def generate_theories():
        t = copy.deepcopy(theories.default_card)
        return [t]

    def doit(self, filename):
        theory_cards = self.generate_theories()
        observable_cards = self.generate_observables()

        for cards in cartesian_product(
            {"theory": theory_cards, "observables": observable_cards}
        ):
            r = yadism.Runner(**cards)
            res = r.get_result()
            res.dump_pineappl_to_file(filename, self.obs_name)


if __name__ == "__main__":
    sand = Pineappl()
    sand.doit("test.pineappl")
