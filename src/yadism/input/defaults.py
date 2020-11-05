# -*- coding: utf-8 -*-
"""
Define the default manager, in order to:

- check if all fields are provided
- apply default for missing fields, warning immediately the user that a default
  is being applied

"""
import warnings

from . import errors


# ┌──────────┐
# │ Defaults │
# └──────────┘


class DefaultManager:
    def __init__(self, default_rule):
        self.default = default_rule

    def __call__(self, user_inputs, missing_yields_error=True):
        var_name = self.default["involve"]
        if var_name in user_inputs:
            return user_inputs

        if self.default["default"] is None:
            import rich

            rich.print(f"[cyan]{var_name}")
            if missing_yields_error:
                raise errors.DefaultError(self.default)
        else:
            msg = f"""The following default is being applied:
                {self.default["involve"]} = {self.default["default"]}"""
            warnings.warn(msg, errors.DefaultWarning)
            user_inputs[var_name] = self.default["default"]

        return user_inputs
