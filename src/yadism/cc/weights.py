# -*- coding: utf-8 -*-
from .. import observable_name as obs_name


class Weights:
    def __init__(self, coupling_constants, Q2, kind, cc_flavor):
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
        #name = obs_name.ObservableName(obs_name.fake_kind + cc_flavor)
        #if name.is_raw_heavy:
        #    active_light_flavors = name.hqnumber - 1
        #else:
        #    active_light_flavors = 6
        #if cc_flavor == "light":
        #    norm = 3
        #else:
        norm = 1

        for q in range(1, 6 + 1):
            sign = 1 if q % 2 == rest else -1
            w = coupling_constants.get_weight(q, Q2, kind, cc_flavor=cc_flavor)
            weights["q"][sign * q] = w if kind != "F3" else sign * w
            tot_ch_sq += w
        # gluon coupling = charge sum
        # TODO: for the light we need: -> why is there a 6?
        # weights["g"][21] = tot_ch_sq / 6
        weights["g"][21] = tot_ch_sq / norm
        self.w = weights


def weight_factory(kind, cc_flavor):
    return lambda coupling_constants, Q2: Weights(
        coupling_constants, Q2, kind, cc_flavor
    )
