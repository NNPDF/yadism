# -*- coding: utf-8 -*-

import re
import textwrap


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

    def __init__(
        self, *, name, description, type, known_as, value, domain_="", **kwargs
    ):
        """Generates the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.
        """
        self.name = name
        self.known_as = known_as
        msg = f"""Following argument outside the domain:
               name: {name}
               known_as: {known_as}
               description:
               DESCRIPTION
               type: {type}
               domain:
               DOMAIN
               value provided: {value}
               """
        domain = "\t" + re.sub("\n", "\n\t\t", domain_)
        description = "\n\t\t".join(
            textwrap.wrap(description.strip(), 66, break_long_words=False)
        )
        msg = re.sub("\n *", "\n\t", msg)
        msg = re.sub("DOMAIN", domain, msg)
        msg = re.sub("DESCRIPTION", f"\t{description}", msg)
        msg = re.sub("\t", "   ", msg)
        self.args = (msg,)
        # raise ValueError


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


class DefaultError(ValueError):
    """Missing argument for field without default"""

    def __init__(self, default):
        """Generate the error message to be reported."""
        self.name = default["name"]
        msg = f"Missing default for the variable `{default['involve']}`"
        self.args = (msg,)


class DefaultWarning(RuntimeWarning):
    """Warn the user that a default is being applied"""

    def __init__(self, msg):
        """Generate the error message to be reported."""

        self.args = (msg,)
