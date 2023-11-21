"""Common factors see :ref:`Larin:1996wd` (Table 2)"""
import numba as nb
import numpy as np

d3 = 1 / 3.0
d9 = 1 / 9.0
d27 = 1.0 / 27.0
d81 = 1.0 / 81.0
d243 = 1.0 / 243.0


def nc_color_factor(coupling_constants, nf, channel, skip_heavylight):
    """Returns the |N3LO| color factor.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    nf : int
        number of active flavors
    channel : str
        partonic channel "ns", "s", "g". Note here "s" means Pure Singlet.
    skip_heavylight : bool
        prevent the last quark to couple to the boson

    Returns
    -------
    weights : dict
        mapping pid -> weight for ns, g and s channel

    """
    pids = range(1, nf + 1)
    w_pc = np.array(
        [coupling_constants.linear_partonic_coupling(pid) for pid in pids], dtype=float
    )
    # if skip_heavylight the last pid couplig is set to 0
    if skip_heavylight:
        w_pc[-1] = 0
    if not w_pc.any():
        return 0
    if channel == "ns":
        return fl(w_pc)
    if channel == "s":
        return fls(w_pc) - fl(w_pc)
    if channel == "g":
        return flg(w_pc)
    raise ValueError(f"NC color factor {channel} is not defined.")


@nb.njit("f8(f8[:])", cache=True)
def fl(nc_weights):
    """:math:`fl_{11}` Non Singlet as defined in :ref:`Larin:1996wd` (Table 2) and generalized for |NC|"""
    # fl = [2.0, 0.5, 0.0, 0.5, 0.2, 0.5]
    avg = np.mean(nc_weights)
    return 3 * avg


@nb.njit("f8(f8[:])", cache=True)
def fls(nc_weights):
    """:math:`fl_{11}` pure Singlet as defined in :ref:`Larin:1996wd` (Table 2) and generalized for |NC|"""
    avg_2 = np.mean(nc_weights) ** 2
    sum_w2 = np.mean(nc_weights**2)
    # fls = [1.0, 0.1, 0.0, 0.1, 0.01818181818, 0.1]
    return avg_2 / sum_w2


@nb.njit("f8(f8[:])", cache=True)
def flg(nc_weights):
    """:math:`fl_{11}^g` pure Singlet as defined in :ref:`Larin:1996wd` (Table 2) and generalized for |NC|"""
    return fls(nc_weights)
