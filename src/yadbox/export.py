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

    # Instantiate the objects required to construct a new Grid
    channels = [pineappl.boc.Channel([([pid], 1.0)]) for pid in output["pids"]]
    first_esf_result = output[obsname][0]
    orders = [pineappl.boc.Order(*o, 0) for o in first_esf_result.orders]
    polarized = obsname.startswith("g")
    convolution_types = pineappl.convolutions.ConvType(
        polarized=polarized, time_like=False
    )
    convolutions = [
        pineappl.convolutions.Conv(convolution_types=convolution_types, pid=2212)
    ]
    kinematics = [pineappl.boc.Kinematics.Scale(0), pineappl.boc.Kinematics.X(0)]
    scale_funcs = pineappl.boc.Scales(
        ren=pineappl.boc.ScaleFuncForm.Scale(0),
        fac=pineappl.boc.ScaleFuncForm.Scale(0),
        frg=pineappl.boc.ScaleFuncForm.NoScale(0),
    )
    bins = len(output[obsname])
    bin_limits = pineappl.boc.BinsWithFillLimits.from_fill_limits(
        fill_limits=list(map(float, range(0, bins + 1)))
    )

    q2grid = np.array([obs.Q2 for obs in output[obsname]])
    interpolations = [
        pineappl.interpolation.Interp(
            min=q2grid.min(),
            max=q2grid.max(),
            nodes=50,
            order=3,
            reweight_meth=pineappl.interpolation.ReweightingMethod.NoReweight,
            map=pineappl.interpolation.MappingMethod.ApplGridH0,
            interpolation_meth=pineappl.interpolation.InterpolationMethod.Lagrange,
        ),  # Interpolation on the Scale
        pineappl.interpolation.Interp(
            min=interpolation_xgrid[0],
            max=interpolation_xgrid[-1],
            nodes=len(interpolation_xgrid),
            order=interpolation_polynomial_degree,
            reweight_meth=pineappl.interpolation.ReweightingMethod.ApplGridX,
            map=pineappl.interpolation.MappingMethod.ApplGridF2,
            interpolation_meth=pineappl.interpolation.InterpolationMethod.Lagrange,
        ),  # Interpolation on momentum fraction x
    ]

    grid = pineappl.grid.Grid(
        pid_basis=pineappl.pids.PidBasis.Pdg,
        channels=channels,
        orders=orders,
        bins=bin_limits,
        convolutions=convolutions,
        interpolations=interpolations,
        kinematics=kinematics,
        scale_funcs=scale_funcs,
    )
    limits = []
    on = observable_name.ObservableName(obsname)
    is_xs = on.kind in observable_name.xs

    # add each ESF as a bin
    for bin_, obs in enumerate(output[obsname]):
        x = obs.x
        Q2 = obs.Q2
        kins = [(Q2, Q2), (x, x)]
        if is_xs:
            kins.append((obs.y, obs.y))
        limits.append(kins)

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
                subgrid = pineappl.subgrid.ImportSubgridV1(
                    array=pid_values[np.newaxis, :],
                    node_values=[[Q2], interpolation_xgrid],
                )
                grid.set_subgrid(order_index, bin_, pid_index, subgrid.into())
    # set the correct observables
    normalizations = [1.0] * bins
    bin_configs = pineappl.boc.BinsWithFillLimits.from_limits_and_normalizations(
        limits=limits,
        normalizations=normalizations,
    )
    grid.set_bwfl(bin_configs)

    # set metadata
    grid.set_metadata("theory", json.dumps(output.theory))
    grid.set_metadata("runcard", json.dumps(output.observables))
    grid.set_metadata("yadism_version", yadism.__version__)
    # set bin information
    grid.set_metadata("x1_label", "Q2")
    grid.set_metadata("x1_label_tex", "$Q^2$")
    grid.set_metadata("x1_unit", "GeV^2")
    grid.set_metadata("x2_label", "x")
    grid.set_metadata("x2_label_tex", "$x$")
    grid.set_metadata("x2_unit", "")
    if is_xs:
        grid.set_metadata("x3_label", "y")
        grid.set_metadata("x3_label_tex", "$y$")
        grid.set_metadata("x3_unit", "")
    grid.set_metadata("y_label", obsname)

    # dump file
    grid.optimize()
    grid.write_lz4(filename)
