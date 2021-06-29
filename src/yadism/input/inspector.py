# -*- coding: utf-8 -*-
"""
The purpose of this module is to provide a runner that implements the semantics
for the input restrictions defined in the following files:

* ``domains.yaml``: in which all the domains restrictions are defined
* ``cross_constraints.yaml``: in which further restrictions are defined,
    each one involving more than one input field
"""

import logging
import pathlib

import yaml

from . import constraints

here = pathlib.Path(__file__).parent

logger = logging.getLogger(__name__)


# ╔═══════════╗
# ║ Inspector ║
# ╚═══════════╝


class Inspector:
    """Instantiate the runner that goes through all constraints.

    Use :func:`check_domains` and :func:`check_cross_constraints` to run the
    check defined respectively in ``domains.yaml`` and
    ``cross_constraints.yaml``.

    Each **default** applied will issue a specific warning.

    Parameters
    ----------
    theory_runcard : dict
        theory inputs from user to inspect and validate
    observables_runcard : dict
        observables inputs from user to inspect and validate

    """

    def __init__(self, theory_runcard, observables_runcard):
        self.theory = theory_runcard
        self.observables = observables_runcard

        domain_file = here / "domains.yaml"
        with open(domain_file, "r") as file:
            self.domains = yaml.safe_load(file)

        cross_constraints_file = here / "cross_constraints.yaml"
        with open(cross_constraints_file, "r") as file:
            self.cross_constraints = yaml.safe_load(file)

    def check_domains(self):
        """
        Iterate over single field constraints (i.e. domains' definitions) and
        immediately raise an error if any input is found outside the boundaries.

        """

        for dom_def in self.domains:
            # load checker with domain definition
            checker = constraints.type_class_map[dom_def["type"]](**dom_def)

            # check value provided by user
            try:
                # retroeve the checker from available checkers and value from
                # user input, apply the first on the latter
                name = dom_def["known_as"] if "known_as" in dom_def else dom_def["name"]
                checker.check_value(
                    value=self.__getattribute__(dom_def["runcard"])[name]
                )
            except KeyError:
                raise ValueError(
                    f"Missing value for '{dom_def['known_as']}' in the input {dom_def['runcard']} runcard"
                )

    def check_cross_constraints(self):
        """
        Iterate over multiple fields constraints (i.e. cross-constraints) and
        immediately raise an error if any input is found outside the boundaries.

        """
        pass

    # def apply_default(self, missing_yields_error=True):
    # """Apply default for missing required arguments"""

    # self.theory = default_manager(self.theory, missing_yields_error)

    def perform_all_checks(self):
        logger.info("Inspecting runcards...")
        self.check_domains()
        self.check_cross_constraints()
        # self.apply_default()
        logger.info("Inspection completed: success ✓")
