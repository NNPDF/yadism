import time
import logging

import numpy as np

from .conv import convolution
from ..coefficient_functions import splitting_functions as split

logger = logging.getLogger(__name__)


class ScaleVariations:
    def __init__(self, order, interpolator):
        self.order = order
        self.interpolator = interpolator
        self.operators = {}
        self.labels = split.labels(self.order)

    def compute_raw(self, label, nf):
        xgrid = self.interpolator.xgrid_raw
        grid_size = len(xgrid)
        # iterate output grid
        for k, xk in enumerate(self.interpolator.xgrid_raw):
            start_time = time.perf_counter()
            # iterate basis functions
            for l, bf in enumerate(self.interpolator):
                if k == l and l == grid_size - 1:
                    continue
                # iterate sectors
                res, err = convolution(split.lo.pqq(nf), xk, bf)
                self.operators[(label, nf)][k][l] = res
            logger.info(
                "computing %s - %d/%d took: %f s",
                label,
                k + 1,
                grid_size,
                time.perf_counter() - start_time,
            )

    def compute_full(self, nf):
        active_labels = ["P_qq_0_0"]
        labels = ["P_qq_0_0"]
        for l in labels:
            self.operators[(l, nf)] = np.zeros((grid_size, grid_size))
        for l in active_labels:
            self.compute_raw(l, nf)
        # fill rank-4 tensor

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
