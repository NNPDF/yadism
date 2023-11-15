import numpy as np
import pathlib

here = pathlib.Path(__file__).parent / "yadism_grids"
here.mkdir(exist_ok=True)

def produce_grids():
    etalist = np.geomspace(1e-6, 1e6, 73, endpoint=True)
    xilist = np.geomspace(1e-3, 1e5, 49, endpoint=True)
    
    np.save(here / "eta.npy", etalist)
    np.save(here / "xi.npy", xilist)

if __name__ == "__main__":
    produce_grids()
