# The plan is:
#     - restrict domains of input fields
#     - implement further restrictions (cross-fields)
#     - apply default
#     - suggest fallbacks
#         - probably is better not to directly implement fallbacks as in APFEL and
#           raise an error consistently if something is not allowed, completely
#           avoiding reporting input (they are exactly the one put in by the user)
#
# make use of the values stored in available.yaml and default.yaml

import os

import yaml

# ┌───────────────────┐
# │ Arguments Classes │
# └───────────────────┘


class Argument:
    """Short summary."""

    pass


class EnumArgument(Argument):
    """Short summary."""

    pass


class RealArgument(Argument):
    """Short summary."""

    pass


# ┌───────────────────────────┐
# │ Cross Constraints Classes │
# └───────────────────────────┘


class CrossConstraint:
    pass


# ╔═══════════╗
# ║ Inspector ║
# ╚═══════════╝


class Inspector:
    """Short summary.

    """

    def __init__():
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.input_dir = os.path.dirname(os.path.realpath(__file__))
        pass

    def check_domains():
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """

        domain_file = os.path.join(self.input_dir, "domain.yaml")
        with open(domain_file, "r") as file:
            domains = yaml.load(file)

    def check_cross_constraints():
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
