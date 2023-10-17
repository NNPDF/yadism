"""Export predictions to PineAPPL."""
import json

import numpy as np

import yadism
from yadism import observable_name


def dump_pineappl_to_file(output, filename, obsname):
    """Write output on a PineAPPL grid file.

    Parameters
    ----------
    filename : str
        output file name
    obsname : str
        observable to be dumped

    """
    # pylint: disable=no-member, too-many-locals
    if len(output[obsname]) <= 0:
        raise ValueError(f"no ESF {obsname}!")
    import pineappl  # pylint: disable=import-outside-toplevel,import-error

    interpolation_xgrid = output["xgrid"]["grid"]
    # interpolation_is_log = self["interpolation_is_log"]
    interpolation_polynomial_degree = output["polynomial_degree"]
    lepton_pid = output["projectilePID"]

    # init pineappl objects
    lumi_entries = [
        pineappl.lumi.LumiEntry([(pid, lepton_pid, 1.0)]) for pid in output["pids"]
    ]
    first_esf_result = output[obsname][0]
    orders = [pineappl.grid.Order(*o) for o in first_esf_result.orders]
    bins = len(output[obsname])
    bin_limits = list(map(float, range(0, bins + 1)))
    # subgrid params
    params = pineappl.subgrid.SubgridParams()
    params.set_reweight(False)
    params.set_x_bins(len(interpolation_xgrid))
    params.set_x_max(interpolation_xgrid[-1])
    params.set_x_min(interpolation_xgrid[0])
    params.set_x_order(interpolation_polynomial_degree)

    grid = pineappl.grid.Grid.create(lumi_entries, orders, bin_limits, params)
    limits = []
    on = observable_name.ObservableName(obsname)
    is_xs = on.kind in observable_name.xs

    # add each ESF as a bin
    for bin_, obs in enumerate(output[obsname]):
        x = obs.x
        Q2 = obs.Q2

        limits.append((Q2, Q2))
        limits.append((x, x))
        if is_xs:
            limits.append((obs.y, obs.y))

        # add all orders
        for o, (v, _e) in obs.orders.items():
            order_index = list(first_esf_result.orders.keys()).index(o)
            prefactor = (
                ((1.0 / (4.0 * np.pi)) ** o[0]) * ((-1.0) ** o[2]) * ((-1.0) ** o[3])
            )
            # add for each pid/lumi
            for pid_index, pid_values in enumerate(v):
                pid_values = prefactor * pid_values
                # grid is empty? skip
                if not any(np.array(pid_values) != 0):
                    continue
                subgrid = pineappl.import_only_subgrid.ImportOnlySubgridV1(
                    pid_values[np.newaxis, :, np.newaxis],
                    [Q2],
                    interpolation_xgrid,
                    [1.0],
                )
                grid.set_subgrid(order_index, bin_, pid_index, subgrid)
    # set the correct observables
    normalizations = [1.0] * bins
    remapper = pineappl.bin.BinRemapper(normalizations, limits)
    grid.set_remapper(remapper)

    # set the initial state PDF ids for the grid
    grid.set_key_value("initial_state_1", "2212")
    grid.set_key_value("initial_state_2", str(lepton_pid))
    grid.set_key_value("theory", json.dumps(output.theory))
    grid.set_key_value("runcard", json.dumps(output.observables))
    grid.set_key_value("yadism_version", yadism.__version__)
    grid.set_key_value("lumi_id_types", "pdg_mc_ids")
    # set bin information
    grid.set_key_value("x1_label", "Q2")
    grid.set_key_value("x1_label_tex", "$Q^2$")
    grid.set_key_value("x1_unit", "GeV^2")
    grid.set_key_value("x2_label", "x")
    grid.set_key_value("x2_label_tex", "$x$")
    grid.set_key_value("x2_unit", "")
    if is_xs:
        grid.set_key_value("x3_label", "y")
        grid.set_key_value("x3_label_tex", "$y$")
        grid.set_key_value("x3_unit", "")
    grid.set_key_value("y_label", obsname)
    grid.set_key_value("polarized", str(obsname.startswith("g")))

    # dump file
    grid.optimize()
    grid.write(filename)
