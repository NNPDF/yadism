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
        for lnf_power in range(alphas_power):
            for lnrf_power in range(alphas_power - 1):
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
        f = len(br.evol_basis)
        l = len(self.interpolator.xgrid)
        zeros = np.zeros((f, l, f, l))
        # collect all elements
        for k, sectors in smap.items():
            # propagete sectors
            fact_op = zeros.copy()
            fact_op[
                br.evol_basis.index("S"), :, br.evol_basis.index("S"), :
            ] = sectors.get("S_qq", 0)
            fact_op[
                br.evol_basis.index("S"), :, br.evol_basis.index("g"), :
            ] = sectors.get("S_qg", 0)
            fact_op[
                br.evol_basis.index("g"), :, br.evol_basis.index("S"), :
            ] = sectors.get("S_gq", 0)
            fact_op[
                br.evol_basis.index("g"), :, br.evol_basis.index("g"), :
            ] = sectors.get("S_gg", 0)
            fact_op[
                br.evol_basis.index("V"), :, br.evol_basis.index("V"), :
            ] = sectors.get("NS_v", 0)
            for q in range(2, nf + 1):
                n = q ** 2 - 1
                fact_op[
                    br.evol_basis.index(f"T{n}"), :, br.evol_basis.index(f"T{n}"), :
                ] = sectors.get("NS_p", 0)
                fact_op[
                    br.evol_basis.index(f"V{n}"), :, br.evol_basis.index(f"V{n}"), :
                ] = sectors.get("NS_m", 0)
            fact_matrices[k] = fact_op
        # rotate back to flavor space
        rot = br.rotate_flavor_to_evolution.copy()

        return fact_matrices

    def fact_to_ren_prefactors(self, nf):
        fact_to_ren_prefactors = {((2, 1), 1): [0.0]}
        return fact_to_ren_prefactors

    def apply_scale_variations(self, ker_orders, nf):
        pass
