"""Implementation of factorization and renormalization scale variations."""
import logging
import time

import numpy as np
from eko import basis_rotation as br
from eko import beta
from scipy.special import binom

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
    """Manager for scale variations."""

    def __init__(self, order, interpolator, activate_ren, activate_fact):
        """Inizialize manager.

        Parameters
        ----------
        order : int
            perturbative order
        interpolator : eko.interpolation.InterpolationDispatcher
            interpolation basis functions
        activate_ren : bool
            activate renormalization scale variation
        activate_fact : bool
            activate factorization scale variation
        """
        self.order = order
        self.interpolator = interpolator
        self.activate_ren = activate_ren
        self.activate_fact = activate_fact
        self.operators = {}
        self.raw_labels = split.raw_labels[: self.order]
        logger.info(
            "RenScaleVar: %s, FactScaleVar: %s", self.activate_ren, self.activate_fact
        )

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
        r"""Compute all matrices related to factorization scale variation, i.e. :math:`\ln(Q^2/\mu_F^2)`.

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
        r"""Provide the renormalization scale variation coefficients, i.e. :math:`\ln(\mu_F^2/\mu_R^2)`.

        Parameters
        ----------
        nf : int
            number of active flavors

        Returns
        -------
        dict :
            map with `(target, lnf2r, src) -> np.ndarray`
        """
        beta0 = beta.beta_qcd_as2(nf)
        ren_coeffs = {
            (2, 1, 1): +beta0,
            (3, 1, 2): +2 * beta0,
            (3, 1, 1): +beta.beta_qcd_as3(nf),
            (3, 2, 1): +(beta0**2),
        }
        return dict(filter(lambda item: item[0][0] <= self.order, ren_coeffs.items()))

    def apply_common_scale_variations(self, ker_orders, nf):
        """
        Add new kernels for common scale varied coefficient functions.

        Parameters
        ----------
            ker_orders : list
                raw (unscale-varied) coefficient functions
            nf : int
                number of active flavors

        Returns
        -------
            list :
                kernels map
        """
        if not self.activate_fact:
            return []
        # get the two ingredients: matrices and projectors
        fmatrices = self.fact_matrices(nf)
        projectors = br.ad_projectors(nf, False)
        # join everything together
        added_ker_sv = []
        for (o, oqed, _, _), ker in ker_orders:
            partons_proj = ker[0][:, 0] @ projectors
            for (target, lnf, src), fmat in fmatrices.items():
                if src == o:
                    val_sv = fmat @ ker[1][0]
                    err_sv = fmat @ ker[2][0]
                    added_ker_sv.append(
                        ((target, oqed, 0, lnf), (partons_proj.T, val_sv, err_sv))
                    )
        return added_ker_sv

    def apply_diff_scale_variations(self, ker_orders, nf):
        """
        Add new kernels for different scale varied coefficient functions.

        Parameters
        ----------
            ker_orders : list
                common-scale varied coefficient functions
            nf : int
                number of active flavors

        Returns
        -------
            Iterable :
                kernels map
        """
        # if none is active - perfect, nothing to do
        if not self.activate_fact and not self.activate_ren:
            return []
        diff_kers = self.apply_raw_diff_scale_variations(ker_orders, nf)
        ren_kers = []
        for o, k in diff_kers:
            # ln((xi_f/xi_r)^2)^n = (ln(xi_f^2) - ln(xi_r^2))^n
            n = o[2]
            for j in range(
                n + 1
            ):  # j is the power of ln(xi_r^2), n-j is the power of ln(xi_f^2)
                binomial = binom(n, j) * (-1) ** j  # take care of the additional minus
                ren_kers.append(
                    ((o[0], o[1], j, n - j + o[3]), (binomial * k[0], k[1], k[2]))
                )
        # if at least one was trivial, skip that one (since the user asked for it)
        if not self.activate_ren:
            return filter(lambda e: e[0][2] == 0, ren_kers)
        if not self.activate_fact:
            return filter(lambda e: e[0][3] == 0, ren_kers)
        # ok, we need to return the full thing
        return ren_kers

    def apply_raw_diff_scale_variations(self, ker_orders, nf):
        """
        Add new kernels for different scale varied coefficient functions.

        Parameters
        ----------
            ker_orders : list
                common-scale varied coefficient functions
            nf : int
                number of active flavors

        Returns
        -------
            list :
                kernels map
        """
        ren_coeffs = self.ren_coeffs(nf)
        # join everything together
        added_ker_sv = []
        for (o, oqed, _, lnf), ker in ker_orders:
            # TODO: APFEL is wrong - fix it temporarily here
            # if (o, lnf) == (1, 1):
            #     continue
            for (target, lnf2r, src), rcoeff in ren_coeffs.items():
                if src == o:
                    added_ker_sv.append(
                        ((target, oqed, lnf2r, lnf), (rcoeff * ker[0], ker[1], ker[2]))
                    )
        return added_ker_sv
