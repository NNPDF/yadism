"""
Defines :py:class:`DistributionVec` and its API, that are used to represent
distribution objects in the coefficient function definition and calculation.

"""

import numpy as np
import scipy.integrate
from eko import interpolation

# TODO: don't use any default
eps_integration_border = 1e-10
"""Set the integration domain restriction, see
:ref:`Integration Note<integration-note>`"""

eps_integration_abs = 1e-13
"""Set the integration target absolute error, see
:ref:`Integration Note<integration-note>`"""


def quad_ker_reg_sing(z, x, is_log, areas, reg, reg_args, sing, pdf_at_x, sing_args):
    if is_log:
        pdf_at_x_ov_z_div_z = interpolation.log_evaluate_x(x / z, areas) / z
    else:
        pdf_at_x_ov_z_div_z = interpolation.evaluate_x(x / z, areas) / z
    # compute
    reg_integrand = reg(z, reg_args) * pdf_at_x_ov_z_div_z
    sing_integrand = sing(z, sing_args) * (pdf_at_x_ov_z_div_z - pdf_at_x)
    return reg_integrand + sing_integrand


def quad_ker_reg(z, x, is_log, areas, reg, reg_args):
    if is_log:
        pdf_at_x_ov_z_div_z = interpolation.log_evaluate_x(x / z, areas) / z
    else:
        pdf_at_x_ov_z_div_z = interpolation.evaluate_x(x / z, areas) / z
    # compute
    reg_integrand = reg(z, reg_args) * pdf_at_x_ov_z_div_z
    return reg_integrand


def quad_ker_sing(z, x, is_log, areas, sing, pdf_at_x, sing_args):
    if is_log:
        pdf_at_x_ov_z_div_z = interpolation.log_evaluate_x(x / z, areas) / z
    else:
        pdf_at_x_ov_z_div_z = interpolation.evaluate_x(x / z, areas) / z
    # compute
    sing_integrand = sing(z, sing_args) * (pdf_at_x_ov_z_div_z - pdf_at_x)
    return sing_integrand


def convolution(rsl, x, pdf_func):
    r"""
    Convolute a :py:class:`yadism.coefficient_functions.partonic_channel.RSL`
    instance with a function ``pdf_func``.

    The definition of the convolution performed is:

    .. math::
        \int_x^{1} \frac{\text{d}z}{z} dvec(z) f\left(\frac{x}{z}\right)

    (notice that is symmetryc in :math:`dvec \leftrightarrow f`).

    .. _integration-note:

    Note
    ----
    The module level attributes :py:attr:`eps_integration_abs` and
    :py:attr:`eps_integration_border` regulate the integration process,
    setting respectively the absolute error and restricting the
    integration domain in order to avoid singularities.

    Parameters
    ----------
    rsl: yadism.coefficient_functions.partonic_channel.RSL
        an object representing a distribution
    x : scalar
        the kinematics point at which the convoution is evaluated
    pdf_func : callable
        the function to be convoluted with ``rsl`` (usually a PDF, or a PDF
        interpolator)

    Returns
    -------
    float
        the result of the convolution
    float
        the integration error

    Note
    ----
    The real name of this function is ``convnd``.
    """
    # empty domain?
    if x >= (1 - eps_integration_border):
        return 0.0, 0.0
    # eko environment?
    if pdf_func.is_below_x(x):
        # support below x --> trivially 0
        return 0.0, 0.0
    else:
        # set breakpoints as relevant points of the integrand
        # computed from interpolation areas of `pdf_func`
        # and also eventually restrict integration domain
        area_borders = []
        for area in pdf_func.areas:
            area_borders.extend([area.xmin, area.xmax])
        area_borders = np.unique(area_borders)
        if pdf_func._mode_log:  # pylint: disable=protected-access
            area_borders = np.exp(area_borders)
        breakpoints = x / area_borders
        z_min = x
        z_max = min(max(breakpoints), 1)

    # cache values
    pdf_at_x = pdf_func(x)

    quad_ker = None
    quad_args = None
    if rsl.reg is not None or rsl.sing is not None:
        quad_args = (
            x,
            pdf_func._mode_log,
            pdf_func.areas_representation,
        )
        if rsl.reg is not None:
            reg_args = (
                rsl.reg,
                rsl.args["reg"],
            )
            quad_args = (*quad_args, *reg_args)
            quad_ker = quad_ker_reg
        if rsl.sing is not None:
            sing_args = (
                rsl.sing,
                pdf_at_x,
                rsl.args["sing"],
            )
            quad_args = (*quad_args, *sing_args)
            quad_ker = quad_ker_sing
        if rsl.reg is not None and rsl.sing is not None:
            quad_ker = quad_ker_reg_sing

    # actual convolution
    # ------------------

    # integrate the kernel, if needed
    if quad_ker is None:
        res, err = 0, 0
    else:
        res, err = scipy.integrate.quad(
            quad_ker,
            z_min * (1 + eps_integration_border),
            z_max * (1 - eps_integration_border),
            args=quad_args,
            epsabs=eps_integration_abs,
            points=breakpoints,
        )

    # sum the addends
    if rsl.loc is None:
        local_at_x = 0
    else:
        local_at_x = rsl.loc(x, rsl.args["loc"])

    res += pdf_at_x * local_at_x

    return res, err


def convolute_operator(fnc, interpolator):
    """
    Convolute function over all basis functions over all grid points.

    Parameters
    ----------
        fnc : RSL
            integration kernel
        interpolator : InterpolationDispatcher
            basis functions

    Returns
    -------
        ls : np.ndarray
            values
        els : np.ndarray
            errors
    """
    xgrid = interpolator.xgrid.raw
    grid_size = len(xgrid)
    op_res = np.zeros((grid_size, grid_size))
    op_err = np.zeros((grid_size, grid_size))
    # iterate output grid
    for k, xk in enumerate(interpolator.xgrid.raw):
        # iterate basis functions
        for l, bf in enumerate(interpolator):
            if k == l and l == grid_size - 1:
                continue
            # iterate sectors
            res, err = convolution(fnc, xk, bf)
            op_res[l, k] = res
            op_err[l, k] = err
    return op_res, op_err


def convolute_vector(cf, interpolator, convolution_point):
    """
    Convolute function over all basis functions.

    Parameters
    ----------
        cf : RSL
            integration kernel
        interpolator : InterpolationDispatcher
            basis functions
        convolution_point : float
            convolution point

    Returns
    -------
        ls : np.ndarray
            values
        els : np.ndarray
            errors
    """
    ls = []
    els = []
    # iterate all polynomials
    for polynomial_f in interpolator:
        c, e = convolution(cf, convolution_point, polynomial_f)
        ls.append(c)
        els.append(e)
    return np.array(ls), np.array(els)
