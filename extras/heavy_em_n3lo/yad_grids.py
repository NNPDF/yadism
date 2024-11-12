import pathlib
import sys
import time
from multiprocessing import Pool

import adani
import numpy as np

here = pathlib.Path(__file__).parent / "yadism_grids"
here.mkdir(exist_ok=True)

nf = int(sys.argv[1])
n_threads = int(sys.argv[2])
kind = sys.argv[3]
if kind not in ["2", "L"]:
    raise ValueError("Set kind to '2' or 'L'")

channel = sys.argv[4]
if channel not in ["q", "g"]:
    raise ValueError("Set channel to 'g' or 'q'")

order = 3

mufrac = 1.0
verbose = True

hs_version = "exact"

massive = adani.ApproximateCoefficientFunction(
    order, kind, channel, True, hs_version
)


def x_eta(eta, m2Q2):
    return 1.0 / (1.0 + 4.0 * m2Q2 * (eta + 1))


def function_to_exe_in_parallel(pair):
    eta, xi = pair
    m2Q2 = 1 / xi
    m2mu2 = 1 / xi
    x = x_eta(eta, m2Q2)

    res = massive.fxBand(x, m2Q2, m2mu2, nf)

    return [res.GetLower(), res.GetCentral(), res.GetHigher()]


def run(n_threads, eta_grid, xi_grid):
    grid = []
    for xi in xi_grid:
        for eta in eta_grid:
            grid.append((eta, xi))
    args = (function_to_exe_in_parallel, grid)
    with Pool(n_threads) as pool:
        result = pool.map(*args)
    return result


if __name__ == "__main__":
    output_files = {}
    for variation in range(-1, 1 + 1):
        output_files[variation] = f"C{kind}{channel}_nf{nf}_var{variation}.npy"
    etafname = here / "eta.npy"
    eta_grid = np.load(etafname)
    xifname = here / "xi.npy"
    xi_grid = np.load(xifname)

    if verbose:
        print(
            f"Computation of the grid for the coefficient function C_{kind}{channel}^{order} for nf = {nf}, and µ/Q = {mufrac}"
        )
        print(f"Size of the grid (eta,xi) = ({len(eta_grid)},{len(xi_grid)})")
        print(
            "This may take a while (depending on the number of threads you chose). In order to spend this time, I would suggest you this interesting view:"
        )
        print("https://www.youtube.com/watch?v=53pG68KCUMI")

    start = time.perf_counter()
    res_vec = np.array(run(n_threads, eta_grid, xi_grid))
    if verbose:
        print("total running time: ", time.perf_counter() - start)

    res_mat = res_vec.reshape(len(xi_grid), len(eta_grid), 3)

    for variation in range(-1, 1 + 1):
        if verbose:
            print(f"Saving {variation} grid in ", here / output_files[variation])
        np.save(here / output_files[variation], res_mat[:, :, variation + 1])
