# -*- coding: utf-8 -*-
from ... import observable_name as obs_name


class Weights:
    def __init__(self, coupling_constants, Q2, cc_flavor):
        weights = {"q": {}, "g": {}}
        # determine couplings
        projectile_pid = coupling_constants.obs_config["projectilePID"]
        if projectile_pid in [-11, 12]:
            rest = 1
        else:
            rest = 0
        # quark couplings
        tot_ch_sq = 0

        # decide the number of active flavors
        name = obs_name.ObservableName(obs_name.fake_kind + cc_flavor)
        if name.is_raw_heavy:
            active_light_flavors = name.hqnumber - 1
        else:
            active_light_flavors = 6

        for q in range(1, active_light_flavors + 1):
            sign = 1 if q % 2 == rest else -1
            w = coupling_constants.get_weight(q, Q2, cc_flavor=cc_flavor)
            # __import__("pdb").set_trace()

            weights["q"][sign * q] = w
            tot_ch_sq += w
        # gluon coupling = charge sum
        weights["g"][21] = tot_ch_sq / 6  # TODO why is there a 6?
        self.w = weights


def weight_factory(cc_flavor):
    return lambda coupling_constants, Q2: Weights(coupling_constants, Q2, cc_flavor)
