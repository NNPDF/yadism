# -*- coding: utf-8 -*-
"""
This module contains the main loop for the DIS calculations.

There are two ways of using ``yadism``:

* ``Runner``: this class provides a runner that get the *theory* and
  *observables* descriptions as input and manage the whole observables'
  calculation process
* ``run_dis``: a function that wraps the construction of a ``Runner`` object
  and calls the proper method to get the requested output

.. todo::
    decide about ``run_dis`` and document it properly in module header
"""

import copy
import inspect
import io
import logging
import time

import rich
import rich.align
import rich.box
import rich.console
import rich.markdown
import rich.panel
import rich.progress
from eko import basis_rotation as br
from eko import thresholds
from eko.interpolation import InterpolatorDispatcher

from . import log, observable_name
from .coefficient_functions.coupling_constants import CouplingConstants
from .esf import scale_variations as sv
from .input import compatibility, inspector
from .output import Output
from .sf import StructureFunction as SF
from .xs import CrossSection as XS

log.setup()
logger = logging.getLogger(__name__)


class Runner:
    """
    Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution (currently
        including PDFSet and DIS process indication).
    observables : dict
        DIS parameters: process description, kinematic specification for the
        requested output.

    Notes
    -----
    For a full description of the content of `theory` and `dis_observables`
    dictionaries read ??.

    .. todo::
        * reference on theory template
        * detailed description of dis_observables entries

    """

    banner = rich.align.Align(
        rich.panel.Panel.fit(
            inspect.cleandoc(
                r"""  __     __       _ _
                     \ \   / /      | (_)
                      \ \_/ /_ _  __| |_ ___ _ __ ___
                       \   / _` |/ _` | / __| '_ ` _ \
                        | | (_| | (_| | \__ \ | | | | |
                        |_|\__,_|\__,_|_|___/_| |_| |_|
                """
            ),
            rich.box.SQUARE,
            padding=1,
            style="magenta",
        ),
        "center",
    )

    def __init__(self, theory: dict, observables: dict):
        # Validate inputs and improve if necessary
        insp = inspector.Inspector(theory, observables)
        insp.perform_all_checks()
        new_theory, new_observables = compatibility.update(theory, observables)

        # Store inputs
        self._theory = new_theory
        self._observables = new_observables

        # Setup eko stuffs
        interpolator = InterpolatorDispatcher.from_dict(self._observables, mode_N=False)

        # Non-eko theory
        coupling_constants = CouplingConstants.from_dict(theory, self._observables)
        # Initialize structure functions
        managers = dict(
            interpolator=interpolator,
            threshold=thresholds.ThresholdsAtlas.from_dict(new_theory, "kDIS"),
            coupling_constants=coupling_constants,
            sv_manager=sv.ScaleVariations(
                order=theory["PTO"],
                interpolator=interpolator,
                activate_ren=new_theory["RenScaleVar"],
                activate_fact=new_theory["FactScaleVar"],
            ),
        )
        # FONLL damping powers
        FONLL_damping = bool(theory["DAMP"])
        if FONLL_damping:
            damping_power = theory.get("DAMPPOWER", 2)  # TODO remove defaults?
            damping_powers = [
                theory.get(f"DAMPPOWER{quark}", damping_power)
                for quark in ("CHARM", "BOTTOM", "TOP")
            ]
        else:
            damping_powers = [2] * 3
        # pass theory params
        intrinsic_range = []
        if theory["IC"] == 1:
            intrinsic_range.append(4)
        theory_params = dict(
            pto=theory["PTO"],
            scheme=theory["FNS"],
            nf_ff=theory["NfFF"],
            ZMq=(new_theory["ZMc"], new_theory["ZMb"], new_theory["ZMt"]),
            intrinsic_range=intrinsic_range,
            m2hq=(theory["mc"] ** 2, theory["mb"] ** 2, theory["mt"] ** 2),
            TMC=theory["TMC"],
            target=new_observables["TargetDIS"],
            GF=theory["GF"],
            M2W=theory["MW"] ** 2,
            M2target=theory["MP"] ** 2,
            FONLL_damping=FONLL_damping,
            damping_powers=damping_powers,
        )
        self.configs = RunnerConfigs(theory=theory_params, managers=managers)
        logger.info("PTO: %d, process: %s", theory["PTO"], new_observables["prDIS"])
        logger.info("FNS: %s, NfFF: %d", theory["FNS"], theory["NfFF"])
        logger.info("Intrinsic: %s", intrinsic_range)
        logger.info(
            "projectile: %s, target: {Z: %g, A: %g}",
            new_observables["ProjectileDIS"],
            *new_observables["TargetDIS"].values(),
        )

        self.observables = {}
        for obs_name, kins in self._observables["observables"].items():
            on = observable_name.ObservableName(obs_name)
            if on.kind in observable_name.xs:
                obs = XS(on, self)
            else:
                # TODO use get_sf?
                obs = SF(on, self)
            # read kinematics
            obs.load(kins)
            self.observables[obs_name] = obs

        # output console
        if log.silent_mode:
            file = io.StringIO()
        else:
            file = None
        self.console = rich.console.Console(file=file)
        # ==============================
        # Initialize output
        # ==============================
        self._output = Output()
        self._output.theory = theory
        self._output.observables = observables
        self._output.update(interpolator.to_dict())
        self._output["pids"] = br.flavor_basis_pids
        self._output["projectilePID"] = coupling_constants.obs_config["projectilePID"]

    def get_sf(self, obs_name):
        if obs_name.name not in self.observables:
            self.observables[obs_name.name] = SF(obs_name, self)
        return self.observables[obs_name.name]

    def get_result(self):
        """
        Compute coefficient functions grid for requested kinematic points.

        Returns
        -------
        :obj:`Output`
            output object, it will store the coefficient functions grid
            (flavour, interpolation-index) for each requested kinematic
            point (x, Q2)

        """
        self.console.print(self.banner)

        # precomputing the plan of calculation
        precomputed_plan = {}
        printable_plan = []
        for name, obs in self.observables.items():
            if name in self._observables["observables"].keys():
                precomputed_plan[name] = obs
                printable_plan.append(
                    f"- {name} at {len(self._observables['observables'][name])} pts"
                )

        self.console.print(rich.markdown.Markdown("## Plan"))
        self.console.print(rich.markdown.Markdown("\n".join(printable_plan)))

        # running the calculation
        self.console.print(rich.markdown.Markdown("## Calculation"))
        self.console.print("yadism took off! please stay tuned ...")
        start = time.time()
        if log.debug:
            for name, obs in precomputed_plan.items():
                self._output[name] = obs.get_result()
        else:
            with rich.progress.Progress(
                transient=True, console=self.console
            ) as progress:
                task = progress.add_task(
                    "Starting...",
                    total=sum(len(obs) for obs in precomputed_plan.values()),
                )
                for name, obs in precomputed_plan.items():
                    results = []
                    for res in obs.iterate_result():
                        results.append(res)
                        progress.update(
                            task,
                            description=f"Computing [bold green]{name}",
                            advance=1,
                        )
                    self._output[name] = results
        end = time.time()
        diff = end - start
        self.console.print(f"[cyan]took {diff:.2f} s")

        out = copy.deepcopy(self._output)
        return out


class RunnerConfigs:
    def __init__(self, theory, managers):
        self.theory = theory
        self.managers = managers

    def __getattribute__(self, name):
        managers = object.__getattribute__(self, "managers")
        if name == "managers":
            return managers
        if name in managers:
            return self.managers[name]

        theory = object.__getattribute__(self, "theory")
        if name == "theory":
            return theory
        if name in theory:
            return theory[name]

        return super().__getattribute__(name)
