# -*- coding: utf-8 -*-
"""
The purpose of this module is to provide a runner that implements the semantics
for the input restrictions defined in the following files:
    * ``domains.yaml``: in which all the domains restrictions are defined
    * ``cross_constraints.yaml``: in which further restrictions are defined,
        each one involving more than one input field
"""

import pathlib

import yaml

from . import constraints

here = pathlib.Path(__file__).parent


# ╔═══════════╗
# ║ Inspector ║
# ╚═══════════╝


class Inspector:
    """Instantiate the runner that goes through all constraints.

    Use :func:`check_domains` and :func:`check_cross_constraints` to run the
    check defined respectively in ``domains.yaml`` and
    ``cross_constraints.yaml``.

    Each **default** applied will issue a specific warning.

    """

    def __init__(self, user_inputs):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.user_inputs = user_inputs

        domain_file = here / "domains.yaml"
        with open(domain_file, "r") as file:
            self.domains = yaml.safe_load(file)

        cross_constraints_file = here / "cross_constraints.yaml"
        with open(cross_constraints_file, "r") as file:
            self.cross_constraints = yaml.safe_load(file)

        defaults_file = here / "defaults.yaml"
        with open(defaults_file, "r") as file:
            self.defaults = yaml.safe_load(file)

    def check_domains(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """

        for dom_def in self.domains:
            # load checker with domain definition
            checker = constraints.type_class_map[dom_def["type"]](**dom_def)

            if checker is None:
                continue

            # check value provided by user
            try:
                name = dom_def["known_as"] if "known_as" in dom_def else dom_def["name"]
                checker.check_value(value=self.user_inputs[name])
            except KeyError:
                # TODO:
                # check if a default exists, if not raise a proper error
                pass

    def check_cross_constraints(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        pass

    def apply_default(self, missing_yields_error=True):
        """Apply default for missing required arguments"""

        for default in self.defaults["simple-defaults"]:
            default_manager = constraints.DefaultManager(default)
            self.user_inputs = default_manager(self.user_inputs, missing_yields_error)

    def perform_all_checks(self):
        self.check_domains()
        self.check_cross_constraints()
        self.apply_default()
