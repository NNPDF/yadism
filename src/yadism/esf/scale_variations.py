import logging
import time

import numpy as np
from eko import basis_rotation as br
from eko import beta

from ..coefficient_functions import splitting_functions as split
from .conv import convolute_operator

logger = logging.getLogger(__name__)


def build_orders(order):
    """
    Compute all necessary order configurations for a given power of alpha.

    Parameters
    ----------
        order : int
            order in pQCD

    Returns
    -------
        orders : list(tuple)
            order configurations
    """
    orders = []
    for alphas_power in range(order + 1):
        for lnf_power in range(alphas_power + 1):
            for lnrf_power in range(max(alphas_power, 1)):
                orders.append((alphas_power, 0, lnrf_power, lnf_power))
    return orders


class ScaleVariations:
    """
    Apply scale variations.

    Parameters
    ----------
        order : int
            perturbative order
        interpolator : eko.interpolation.InterpolationDispatcher
            interpolation basis functions
    """

    def __init__(self, order, interpolator):
        self.order = order
        self.interpolator = interpolator
        self.operators = {}
        self.raw_labels = split.raw_labels[: self.order]

    def compute_raw(self, nf):
        """
        Compute all basic building blocks.

        Parameters
        ----------
            nf : int
                number of active flavors
        """
        # compute all raw ingredients
        for order_labels in self.raw_labels:
            for l, fnc in order_labels.items():
                if (l, nf) in self.operators:
                    logger.debug("using cached %s", l)
                    continue
                start_time = time.perf_counter()
                # TODO add error propagation
                res, _err = convolute_operator(fnc(nf), self.interpolator)
                self.operators[(l, nf)] = res
                logger.info(
                    "computing %s - took: %f s", l, time.perf_counter() - start_time
                )

    def fact_matrices(self, nf):
        r"""
        Compute all matrices related to factorization scale variation,
        i.e. :math:`\ln(Q^2/\mu_F^2)`.

        Parameters
        ----------
            nf : int
                number of active flavors

        Returns
        -------
            dict :
                map with `(target, lnf, src) -> np.ndarray`
        """
        self.compute_raw(nf)
        # load mappings
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

    def ren_coeffs(self, nf):
        r"""
        Provide the renormalization scale variation coefficients,
        i.e. :math:`\ln(\mu_F^2/\mu_R^2)`.

        Parameters
        ----------
            nf : int
                number of active flavors

        Returns
        -------
            dict :
                map with `(target, lnf2r, src) -> np.ndarray`

        """
        ren_coeffs = {(2, 1, 1): -beta.beta_0(nf)}
        return dict(filter(lambda item: item[0][0] <= self.order, ren_coeffs.items()))

    def apply_common_scale_variations(self, ker_orders, nf):
        """
        Add new kernels for common scale varied coefficient functions.

        Parameters
        ----------
            ker_orders : dict
                raw (unscale-varied) coefficient functions
            nf : int
                number of active flavors

        Returns
        -------
            dict :
                kernels map
        """
        # get the two ingredients: matrices and projectors
        fmatrices = self.fact_matrices(nf)
        projectors = br.ad_projectors(nf)
        # join everything together
        ker_sv = {}
        for (o, oqed, _, _), ker in ker_orders.items():
            partons_proj = ker[0][:, 0] @ projectors
            for (target, lnf, src), fmat in fmatrices.items():
                if src == o:
                    val_sv = fmat @ ker[1][0]
                    err_sv = fmat @ ker[2][0]
                    ker_sv[(target, oqed, 0, lnf)] = (partons_proj.T, val_sv, err_sv)
        return ker_sv

    def apply_diff_scale_variations(self, ker_orders, nf):
        """
        Add new kernels for different scale varied coefficient functions.

        Parameters
        ----------
            ker_orders : dict
                common-scale varied coefficient functions
            nf : int
                number of active flavors

        Returns
        -------
            dict :
                kernels map
        """
        ren_coeffs = self.ren_coeffs(nf)
        # join everything together
        ker_sv = {}
        for (o, oqed, _, lnf), ker in ker_orders.items():
            for (target, lnf2r, src), rcoeff in ren_coeffs.items():
                if src == o:
                    ker_sv[(target, oqed, lnf2r, lnf)] = (
                        rcoeff * ker[0],
                        ker[1],
                        ker[2],
                    )
        return ker_sv
