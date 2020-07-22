# -*- coding: utf-8 -*-

class WeightLight:
    def __init__(self, pids, coupling_constants, Q2):
        weights = {"q": {}, "g": {}}
        # quark couplings
        tot_ch_sq = 0
        for q in pids:  # u+d+s
            w = coupling_constants.get_weight(q, Q2)
            weights["q"][q] = w
            weights["q"][-q] = w
            tot_ch_sq += w
        # gluon coupling = charge average (omitting the *2/2)
        weights["g"][21] = tot_ch_sq / 3  # 3 = u+d+s
        self.w = weights

class WeightHeavy:
    def __init__(self, nhq, coupling_constants, Q2):
        weight_vv = coupling_constants.get_weight(nhq, Q2, "V")
        weight_aa = coupling_constants.get_weight(nhq, Q2, "A")
        weights = {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}}
        self.w = weights

def light_factory(pids):
    return lambda coupling_constants, Q2: WeightLight(pids, coupling_constants, Q2)

def heavy_factory(nhq):
    return lambda coupling_constants, Q2: WeightHeavy(nhq, coupling_constants, Q2)
