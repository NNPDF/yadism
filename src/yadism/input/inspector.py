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

import abc
import os

import yaml

# ┌───────────────────┐
# │ Arguments Classes │
# └───────────────────┘


class DomainError(ValueError):
    """Error raised while checking inputs (single argument violation).

    Parameters
    ----------
    name : str
        Name of the input variable.
    description : str
        Domain description provided.
    domain : :obj:`list`, optional
        The set of rules used to provide .

    .. todo::
        format domain properly according the type, this should be done by
        error Argument subclasses before raising.
    """

    def __init__(self, *, name, description, domain=None):
        """Generates the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.

        ..todo::
            define the actual format
        """
        self.args = (name + description,)


class Argument(abc.ABC):
    """Base Class for input variables' domains semantics definition.

    Parameters
    ----------
    **kwargs
        Domain specification, with the syntax defined in ``domains.yaml``."""

    def __init__(self, **kwargs):
        """Load ``kwargs`` as object attributes."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def check_value(*, value):
        """Perform the actual check .

        Parameters
        ----------
        value : type
            Description of parameter `value`.
        """
        pass

    @abc.abstractmethod
    def __raise_error():
        """Raise the error, preprocessing the message."""
        pass


class EnumArgument(Argument):
    """Short summary."""

    def check_value(*, value):
        if value not in self.domain:
            raise ArgumentError()

    def __raise_error():
        pass


class RealArgument(Argument):
    """Short summary."""

    def check_value(*, value):
        pass


# ┌───────────────────────────┐
# │ Cross Constraints Classes │
# └───────────────────────────┘


class CrossConstraintError(ValueError):
    """Error raised while checking inputs (more arguments involved)."""

    def __init__(self):
        """Generate the error message to be included in the Traceback."""
        pass


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
