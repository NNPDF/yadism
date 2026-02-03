import pathlib

import numpy as np
from scipy.interpolate import NearestNDInterpolator, RectBivariateSpline

grid_path = pathlib.Path(__file__).parent / "grids"

eta_grid = np.load(grid_path / "eta.npy")
xi_grid = np.load(grid_path / "xi.npy")

interpolators = {}


def fill_nans_nearest_neighbor(xi_grid, eta_grid, coeffs):
    z_filled = coeffs.copy()
    mask = np.isfinite(coeffs)
    values = coeffs[mask]

    xm, ym = np.meshgrid(xi_grid, eta_grid, indexing="ij")
    points = np.column_stack((xm[mask], ym[mask]))

    interp_nn = NearestNDInterpolator(points, values)
    z_filled[~mask] = interp_nn(xm[~mask], ym[~mask])
    assert np.all(np.isfinite(z_filled))

    return z_filled


def interpolator(coeff, nf, variation):
    grid_name = f"{coeff}_nf{int(nf)}_var{int(variation)}.npy"

    # is it already loaded ?
    if grid_name in interpolators:
        return interpolators[grid_name]

    # load grid
    coeff = np.load(grid_path / grid_name)
    if np.isnan(coeff).sum() != 0:
        coeff = fill_nans_nearest_neighbor(xi_grid, eta_grid, coeff)
    grid_interpolator = RectBivariateSpline(xi_grid, eta_grid, coeff)

    # store result
    interpolators[grid_name] = grid_interpolator

    return grid_interpolator
