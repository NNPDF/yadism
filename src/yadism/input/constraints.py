# -*- coding: utf-8 -*-
# pylint: skip-file
import abc

import numpy as np

from . import errors

# ┌───────────────────┐
# │ Arguments Classes │
# └───────────────────┘


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


class StringArgument(Argument):
    """Argument definition for ``string`` type.

    ``string`` is the argument type for a generic string, and no other check is
    performed other than verifying that it is loaded just as a plain string and
    not any other kind, that should be managed by a more specific `Argument`
    checker.
    """

    def check_value(self, *, value):
        """Checks if `value` is actually a bare string.

        Raises
        ------
        DomainError
            If `value` is not in the domain of the ``type``.
        """

        if not isinstance(value, str):
            self._raise_error(value)

    def _raise_error(self, value):
        """Wrapper for DomainError, pretty print `domain`.

        No domain rule supported, if needed please choose a more specific
        argument type.
        """
        self.domain_ = ""
        raise errors.DomainError(value=value, **self.__dict__)


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
        """Wrapper for DomainError, pretty print `domain`.

        The domain is formatted as a dashed list.
        """
        dom = list(map(str, self.domain))
        self.domain_ = "- " + "\n- ".join(dom)
        raise errors.DomainError(value=value, **self.__dict__)


class RealArgument(Argument):
    """Argument definition for ``real`` type.

    Actually just a real with restrictions on the domain, so an interval or the
    union of more disconnected intervals.
    """

    def check_value(self, *, value):
        """Checks if `value` belongs to the domain.

        It checks if `value` belongs to any interval available for the domain.

        Raises
        ------
        DomainError
            If `value` is not in the domain of the ``type``.
        """
        # load the value in the namespace with the name used in rules
        try:
            var_name = self.metavar
        except AttributeError:
            var_name = self.known_as

        # NOTE: the value is the only thing user provided, so it will be parsed
        # before to make sure it's nothing else than a float: with this check
        # `exec` is safe
        value = float(value)
        exec(f"{var_name} = {value}")

        # determine to which intervals value belongs to
        intervals = []
        for rule in self.domain:
            # NOTE: rule is a part of `yadism`, so `eval` is safe
            intervals += [eval(rule)]

        # NOTE: multiple conditions are in OR (not in AND)
        if not any(intervals):
            self._raise_error(value)

    def _raise_error(self, value):
        """Wrapper for DomainError, pretty print `domain`.

        The domain is formatted as a dashed list of rules.
        """
        dom = list(map(str, self.domain))
        self.domain_ = "- " + "\n- ".join(dom)
        raise errors.DomainError(value=value, **self.__dict__)


class IntegerArgument(RealArgument):
    """Short summary."""

    def check_value(self, *, value):
        value = float(value)
        value_int = np.round(value)
        if np.abs(value - value_int) > 1e-5:
            self._raise_error(value)
        super(IntegerArgument, self).check_value(value=value_int)


type_class_map = {
    "string": StringArgument,
    "enum": EnumArgument,
    "real": RealArgument,
    "integer": IntegerArgument,
}

# ┌───────────────────────────┐
# │ Cross Constraints Classes │
# └───────────────────────────┘


class CrossConstraint(abc.ABC):
    pass
