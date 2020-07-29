# -*- coding: utf-8 -*-


class WeightLight:
    def __init__(self, pids, coupling_constants, Q2, kind):
        weights = {"q": {}, "g": {}}
        # quark couplings
        tot_ch_sq = 0
        for q in pids:  # u+d+j
            w = coupling_constants.get_weight(q, Q2, kind)
            weights["q"][q] = w
            weights["q"][-q] = w if kind != "F3" else -w
            tot_ch_sq += w
        # gluon coupling = charge average (omitting the *2/2)
        weights["g"][21] = tot_ch_sq / 3  # 3 = u+d+s
        self.w = weights


class WeightHeavy:
    def __init__(self, nhq, coupling_constants, Q2, kind):
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
        self.w = weights


def light_factory(kind, pids):
    return lambda coupling_constants, Q2: WeightLight(
        pids, coupling_constants, Q2, kind
    )


def heavy_factory(kind, nhq):
    return lambda coupling_constants, Q2: WeightHeavy(nhq, coupling_constants, Q2, kind)
