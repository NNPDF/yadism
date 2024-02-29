import pathlib

import numpy as np
from scipy.interpolate import RectBivariateSpline

grid_path = pathlib.Path(__file__).parent / "grids"

eta_grid = np.load(grid_path / "eta.npy")
xi_grid = np.load(grid_path / "xi.npy")

interpolators = {}


def interpolator(coeff, nf, variation):
    grid_name = f"{coeff}_nf{int(nf)}_var{int(variation)}.npy"

    # is it already loaded ?
    if grid_name in interpolators:
        return interpolators[grid_name]

    # load grid
    coeff = np.load(grid_path / grid_name)
    grid_interpolator = RectBivariateSpline(xi_grid, eta_grid, coeff)

    # store result
    interpolators[grid_name] = grid_interpolator

    return grid_interpolator
