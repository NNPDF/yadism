import numpy as np


class ScaleVariations:
    def __init__(self, order, interpolator):
        self.order = order
        self.interpolator = interpolator

    def fact_matrices(self, nf):
        xgrid = self.interpolator.xgrid
        l = len(xgrid)
        # prepare scale variations
        fact_matrices = {
            ((1, 1), 0): np.zeros((l, l)),
            ((2, 1), 0): np.zeros((l, l)),
            ((2, 1), 1): np.zeros((l, l)),
            ((2, 2), 0): np.zeros((l, l)),
        }
        return fact_matrices

    def fact_to_ren_prefactors(self, nf):
        fact_to_ren_prefactors = {((2, 1), 1): [0.0]}
        return fact_to_ren_prefactors
