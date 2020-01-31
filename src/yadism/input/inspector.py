# -*- coding: utf-8 -*-
"""
The purpose of this module is to provide a runner that implements the semantics
for the input restrictions defined in the following files:
    * ``domains.yaml``: in which all the domains restrictions are defined
    * ``cross_constraints.yaml``: in which further restrictions are defined,
        each one involving more than one input field
"""

import abc
import os
import re
import textwrap

import yaml

# ┌───────────────────┐
# │ Arguments Classes │
# └───────────────────┘


class DomainError(ValueError):
    """Error raised while checking inputs (single argument violation).

    .. todo::
        format domain properly according the type, this should be done by
        error Argument subclasses before raising.

    Parameters
    ----------
    name : str
        Name of the input variable.
    description : str
        Domain description provided.
    domain : list, optional
        The set of rules used to provide .
    """

    def __init__(self, *, name, description, known_as, value, domain=None, **kwargs):
        """Generates the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.
        """
        self.name = known_as
        msg = f"""Following argument outside the domain:
               name: {known_as}
               description:
               DESCRIPTION
               domain:
               DOMAIN
               value provided: {value}
               """
        domain = "\t" + re.sub("\n", "\n\t\t", domain)
        description = "\n\t\t".join(
            textwrap.wrap(description.strip(), 66, break_long_words=False)
        )
        msg = re.sub("\n *", "\n\t", msg)
        msg = re.sub("DOMAIN", domain, msg)
        msg = re.sub("DESCRIPTION", f"\t{description}", msg)
        msg = re.sub("\t", "   ", msg)
        self.args = (msg,)
        # raise ValueError


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
    def check_value(self, *, value):
        """Check if ``value`` belongs to the domain.

        Parameters
        ----------
        value : type
            Description of parameter `value`.
        """
        pass

    @abc.abstractmethod
    def _raise_error(self):
        """Raise the error, preprocessing the message."""
        pass


class EnumArgument(Argument):
    """Argument definition for ``enum`` type.

    ``enum`` type is just a domain defined by enumerating all the possible
    values.
    There is no hard-coded restrictions in having in the same enum domain values
    from different default types (e.g. integers and strings may be mixed).
    """

    def check_value(self, *, value):
        """Checks if `value` belongs to the domain.

        It checks if `value` is in the list of the enumerated values available
        for the ``type``.

        Raises
        ------
        DomainError
            If `value` is not in the domain of the ``type``.
        """

        if value not in self.domain:
            self._raise_error(value)

    def _raise_error(self, value):
        """Wrapper for DomainError, pretty print `domain`."""
        dom = list(map(str, self.domain))
        self.domain = "- " + "\n- ".join(dom)
        raise DomainError(value=value, **self.__dict__)


class RealArgument(Argument):
    """Argument definition for ``real`` type.

    Actually just a real with restrictions on the domain, so an interval or the
    union of more disconnected intervals.
    """

    def check_value(self, *, value):
        """Checks if `value` belongs to the domain.

        It checks if `value` is in the list of the enumerated values available
        for the ``type``.

        Raises
        ------
        DomainError
            If `value` is not in the domain of the ``type``.
        """
        # load the value in the namespace with the name used in rules
        if hasattr(self, "metavar") and self.metavar:
            var_name = self.metavar
        else:
            var_name = self.name

        exec(f"{var_name} = {value}")

        # determine to which intervals value belongs to
        intervals = []
        for rule in self.domain:
            intervals += [eval(rule)]

        if not any(intervals):
            self._raise_error(value)

    def _raise_error(self, value):
        """Wrapper for DomainError, pretty print `domain`."""
        dom = list(map(str, self.domain))
        self.domain = "- " + "\n- ".join(dom)
        raise DomainError(value=value, **self.__dict__)


type_class_map = {"enum": EnumArgument, "real": RealArgument}

# ┌───────────────────────────┐
# │ Cross Constraints Classes │
# └───────────────────────────┘


class CrossConstraintError(ValueError):
    """Error raised while checking inputs (more arguments involved)."""

    def __init__(self):
        """Generate the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.

        ..todo::
            * define the arguments involved
            * define the actual format
        """
        pass


class CrossConstraint(abc.ABC):
    pass


# ╔═══════════╗
# ║ Inspector ║
# ╚═══════════╝


class Inspector:
    """Instantiate the runner that goes through all constraints.

    Use :func:`check_domains` and :func:`check_cross_constraints` to run the
    check defined respectively in ``domains.yaml`` and
    ``cross_constraints.yaml``.
    """

    def __init__(self, user_inputs):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.input_dir = os.path.dirname(os.path.realpath(__file__))
        self.user_inputs = user_inputs

    def check_domains(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """

        domain_file = os.path.join(self.input_dir, "domains.yaml")
        with open(domain_file, "r") as file:
            domains = yaml.safe_load(file)

        for dom_def in domains:
            # load checker with domain definition
            checker = type_class_map[dom_def["type"]](**dom_def)
            # check value provided by user
            try:
                checker.check_value(value=self.user_inputs[dom_def["known_as"]])
            except KeyError:
                # @todo `try` to be replaced by an actual error: all the
                # arguments must by supplied
                pass

    def check_cross_constraints(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        pass
