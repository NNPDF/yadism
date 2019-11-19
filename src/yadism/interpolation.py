# -*- coding: utf-8 -*-
"""
This file provides all necessary tools for PDF interpolation.

The files provides the tools for generating grids and the
Lagrange interpolation polynomials

"""
import numpy as np
import numba as nb
from numpy.polynomial import Polynomial as P
from eko import t_float


def get_Lagrange_basis_functions(xgrid_in, polynom_rank: int):
    """Setup all basis function for the interpolation

    Parameters
    ----------
      xgrid_in : array
        Grid in x-space from which the interpolaters are constructed
      polynom_rank : int
        degree of the interpolation polynomial

    Returns
    -------
      list_of_basis_functions : array
        list with configurations for all basis functions
    """
    # setup params
    xgrid = np.unique(xgrid_in)
    xgrid_size = len(xgrid)
    if not len(xgrid_in) == xgrid_size:
        raise ValueError("xgrid is not unique")
    if xgrid_size < 2:
        raise ValueError("xgrid needs at least 2 points")
    if polynom_rank < 1:
        raise ValueError("need at least linear interpolation")
    if xgrid_size < polynom_rank:
        raise ValueError(
            f"to interpolate with rank {polynom_rank} we need at"
            + "least that much points"
        )

    # create blocks
    list_of_blocks = []
    for j in range(xgrid_size - 1):
        kmin = max(0, j - polynom_rank // 2)  # borders are (]
        kmax = kmin + polynom_rank
        if kmax >= xgrid_size:
            kmax = xgrid_size - 1
            kmin = kmax - polynom_rank
        list_of_blocks.append((kmin, kmax))

    # setup basis functions
    list_of_basis_functions = []
    for j in range(xgrid_size):
        areas = []
        for k in range(xgrid_size - 1):
            areas.append({"lower_index": k, "reference_indices": None})
        list_of_basis_functions.append({"polynom_number": j, "areas": areas})
    for j, current_block in enumerate(list_of_blocks):
        for k in range(current_block[0], current_block[1] + 1):
            list_of_basis_functions[k]["areas"][j]["reference_indices"] = current_block
    # compute coefficients
    def is_not_zero_sector(e):
        return not e["reference_indices"] is None

    for j, current_polynom in enumerate(list_of_basis_functions):
        # clean up zero sectors
        current_polynom["areas"] = list(
            filter(is_not_zero_sector, current_polynom["areas"])
        )
        # precompute coefficients
        xj = xgrid[j]
        for current_area in current_polynom["areas"]:
            denominator = 1.0
            coeffs = np.array([1])
            for k in range(
                current_area["reference_indices"][0],
                current_area["reference_indices"][1] + 1,
            ):
                if k == j:
                    continue
                xk = xgrid[k]
                # Lagrange interpolation formula
                denominator *= xj - xk
                x_coeffs = np.insert(coeffs, 0, 0)
                Mxk_coeffs = -xk * coeffs
                Mxk_coeffs = np.append(
                    Mxk_coeffs, np.zeros(len(x_coeffs) - len(Mxk_coeffs))
                )
                coeffs = x_coeffs + Mxk_coeffs
            # apply common denominator
            coeffs = coeffs / denominator
            # save in dictionary
            current_area["coeffs"] = coeffs
            current_area["xmin"] = xgrid[current_area["lower_index"]]
            current_area["xmax"] = xgrid[current_area["lower_index"] + 1]
            # clean up
            del current_area["reference_indices"]
            del current_area["lower_index"]
            # we still need polynom_number as the first polynom has borders [], to allow for testing
    # return all functions
    return list_of_basis_functions


def evaluate_Lagrange_basis_function_x(x, conf):
    """Get a single Lagrange interpolator in x-space

    .. math::
      \\tilde P(x)

    Parameters
    ----------
      x : t_float
        Evaluated point
      conf : dict
        dictionary of values for the coefficients of the interpolator

    Returns
    -------
      p(x) : t_float
        Evaluated polynom at x
    """
    if not "areas" in conf or len(conf["areas"]) <= 0:
        raise ValueError("need some areas to explore")
    # search
    for current_area in conf["areas"]:
        # borders are usually (] - except for the first
        if conf["polynom_number"] == 0:
            if x < current_area["xmin"]:
                continue
        else:
            if x <= current_area["xmin"]:
                continue
        if x > current_area["xmax"]:
            continue
        # match found
        res = 0.0
        for k, coeff in enumerate(current_area["coeffs"]):
            res += coeff * x ** k
        return res
    # no match
    return 0.0

def get_Lagrange_basis_functions_log(xgrid_in, polynom_rank: int):
    """Setup all basis function for logarithmic interpolation

    See Also
    --------
      get_Lagrange_basis_functions
    """
    return get_Lagrange_basis_functions(np.log(xgrid_in), polynom_rank)


def evaluate_Lagrange_basis_function_log_x(x, conf):
    """Get a single, logarithmic Lagrange interpolator in x-space

    .. math::
      \\tilde P^{\\ln}(x)

    Parameters
    ----------
      x : t_float
        Evaluated point
      conf : dict
        dictionary of values for the coefficients of the interpolator

    Returns
    -------
      p(x) : t_float
        Evaluated polynom at x
    """
    return evaluate_Lagrange_basis_function_x(np.log(x), conf)
