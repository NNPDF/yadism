# -*- coding: utf-8 -*-
"""
Note
----
Brief proof of @F3-sign@ for singlet and non-singlet combinations

- sf = F3
- q = 2 (i.e. u-quark)
- q%2 = 2%2 = 0

projectile = e+ -> rest = 1
- sign = -1
- weight[2] is not set (i.e. 0)
- weight[-2] = -w

projectile = e- -> rest = 0
- sign = 1
- weight[2] = w
- weight[-2] is not set

together
- weight[2] + weight[-2] changes sign
- weight[2] - weight[-2] does NOT change sign

"""


def weights(obs_name, coupling_constants, Q2):
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
    if obs_name.flavor == "light":
        norm = 3
    else:
        norm = 1

    for q in range(1, 6 + 1):
        sign = 1 if q % 2 == rest else -1
        w = coupling_constants.get_weight(
            q, Q2, obs_name.kind, cc_flavor=obs_name.raw_flavor
        )
        # @F3-sign@
        weights["q"][sign * q] = w if obs_name.kind != "F3" else sign * w
        tot_ch_sq += w
    # gluon coupling = charge sum
    if rest == 0 and obs_name.kind == "F3":
        tot_ch_sq *= -1
    weights["g"][21] = tot_ch_sq / norm / 2
    return weights
