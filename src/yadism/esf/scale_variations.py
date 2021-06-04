import time
import logging

import numpy as np

from eko import basis_rotation as br

from .conv import convolute_operator
from ..coefficient_functions import splitting_functions as split

logger = logging.getLogger(__name__)


def build_orders(order):
    orders = []
    for alphas_power in range(order + 1):
        for lnf_power in range(alphas_power + 1):
            for lnrf_power in range(max(alphas_power - 1, 1)):
                orders.append((alphas_power, 0, lnrf_power, lnf_power))
    return orders


class ScaleVariations:
    def __init__(self, order, interpolator):
        self.order = order
        self.interpolator = interpolator
        self.operators = {}
        self.raw_labels = split.raw_labels[: self.order]

    def compute_raw(self, nf):
        # compute all raw ingredients
        for order_labels in self.raw_labels:
            for l, fnc in order_labels.items():
                if (l, nf) in self.operators:
                    logger.info("using cached %s", l)
                    continue
                start_time = time.perf_counter()
                res, err = convolute_operator(fnc(nf), self.interpolator)
                self.operators[(l, nf)] = res
                logger.info(
                    "computing %s - took: %f s", l, time.perf_counter() - start_time
                )

    def fact_matrices(self, nf):
        self.compute_raw(nf)
        # fill rank-4 tensor
        smap = split.sector_mapping(self.order, self.operators, nf)
        fact_matrices = {}
        # collect all elements
        for k, sectors in smap.items():
            # propagete sectors
            fact_op = []
            for ad in br.anomalous_dimensions_basis:
                fact_op.append(sectors[ad])
            fact_matrices[k] = np.array(fact_op)

        return fact_matrices

    def fact_to_ren_prefactors(self, nf):
        fact_to_ren_prefactors = {((2, 1), 1): [0.0]}
        return fact_to_ren_prefactors

    def apply_scale_variations(self, ker_orders, nf):
        fmatrices = self.fact_matrices(nf)
        projectors = br.ad_projectors(nf)

        ker_sv = {}

        for (o, _, _, _), ker in ker_orders.items():
            partons_proj = ker[0][:, 0] @ projectors
            for (target, lnf, src), fmat in fmatrices.items():
                if src == o:
                    val_sv = fmat @ ker[1][0]
                    err_sv = fmat @ ker[2][0]
                    ker_sv[(target, 0, 0, lnf)] = (partons_proj.T, val_sv, err_sv)

        return ker_sv
