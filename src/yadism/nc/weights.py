# -*- coding: utf-8 -*-


def weights_light(pids, coupling_constants, Q2, kind):
    weights = {"q": {}, "g": {}}
    # quark couplings
    tot_ch_sq = 0
    for q in pids:  # for light = u+d+s
        w = coupling_constants.get_weight(q, Q2, kind)
        weights["q"][q] = w
        weights["q"][-q] = w if kind != "F3" else -w
        tot_ch_sq += w
    # gluon coupling = charge average (omitting the *2/2)
    weights["g"][21] = tot_ch_sq / len(pids)  # for light = 3 = u+d+s
    return weights


def weights_heavy(nhq, coupling_constants, Q2, kind):
    if kind != "F3":
        weight_vv = coupling_constants.get_weight(nhq, Q2, kind, "V")
        weight_aa = coupling_constants.get_weight(nhq, Q2, kind, "A")
        weights = {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}}
    else:
        weights = {"qVA": {}}
        for q in range(1, nhq):
            w = coupling_constants.get_weight(q, Q2, kind)
            weights["qVA"][q] = w
            weights["qVA"][-q] = -w
    return weights
