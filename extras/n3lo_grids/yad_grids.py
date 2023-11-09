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
channel = sys.argv[3]
order = int(sys.argv[4])
try:
    variation = int(sys.argv[5])
except IndexError:
    variation = 0
mufrac = 1.0
verbose = True


def function_to_exe_in_parallel(pair):
    x, xi = pair
    m2Q2 = 1 / xi
    m2mu2 = 1 / xi
    if order == 3:
        if channel == "2g":
            return adani.C2_g3_approximation(
                x, m2Q2, m2mu2, nf, v=variation, method_flag=1
            )
        elif channel == "2q":
            return adani.C2_ps3_approximation(x, m2Q2, m2mu2, nf, v=variation)
        elif channel == "Lg":
            return adani.CL_g3_approximation(
                x, m2Q2, m2mu2, nf, v=variation, method_flag=1
            )
        elif channel == "Lq":
            return adani.CL_ps3_approximation(x, m2Q2, m2mu2, nf, v=variation)
        else:
            raise ValueError("Set channel to one of these: 2g 2q Lg Lq")
    ## NNLO approximated
    elif order == 2:
        if channel == "2g":
            return adani.C2_g2_approximation(x, m2Q2, m2mu2, v=variation)
        elif channel == "2q":
            return adani.C2_ps2_approximation(x, m2Q2, m2mu2, v=variation)
        elif channel == "Lg":
            return adani.CL_g2_approximation(x, m2Q2, m2mu2, v=variation)
        elif channel == "Lq":
            return adani.CL_ps2_approximation(x, m2Q2, m2mu2, v=variation)
        else:
            raise ValueError("Set channel to one of these: 2g 2q Lg Lq")
    ## NNLO exact
    elif order == 0:
        if channel == "2g":
            return adani.C2_g2(x, m2Q2, m2mu2)
        elif channel == "2q":
            return adani.C2_ps2(x, m2Q2, m2mu2)
        elif channel == "Lg":
            return adani.CL_g2(x, m2Q2, m2mu2)
        elif channel == "Lq":
            return adani.CL_ps2(x, m2Q2, m2mu2)
        else:
            raise ValueError("Set channel to one of these: 2g 2q Lg Lq")


def run(n_threads, x_grid, xi_grid):
    grid = []
    for xi in xi_grid:
        for x in x_grid:
            grid.append((x, xi))
    args = (function_to_exe_in_parallel, grid)
    with Pool(n_threads) as pool:
        result = pool.map(*args)
    return result


if __name__ == "__main__":
    output_file = f"C{channel}_nf{nf}_var{variation}.npy"
    xfname = here / "x.npy"
    x_grid = np.load(xfname)
    xifname = here / "xi.npy"
    xi_grid = np.load(xifname)

    if verbose:
        print(
            f"Computation of the grid for the coefficient function C{channel} for nf = {nf}, and µ/Q = {mufrac}, variation = {variation}"
        )
        print(f"Size of the grid (x,xi) = ({len(x_grid)},{len(xi_grid)})")
        print(
            "This may take a while (depending on the number of threads you choose). In order to spend this time, I would suggest you this interesting view:"
        )
        print("https://www.youtube.com/watch?v=53pG68KCUMI")

    start = time.perf_counter()
    res_vec = np.array(run(n_threads, x_grid, xi_grid))
    if verbose:
        print("total running time: ", time.perf_counter() - start)

    res_mat = res_vec.reshape(len(xi_grid), len(x_grid))
    if verbose:
        print("Saving grid in ", output_file)
    np.save(here / output_file, res_mat)
