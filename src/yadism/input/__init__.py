# -*- coding: utf-8 -*-
"""
Goal
----

These subpackage has the main goal of parsing and validate user input, in
particular the following three operations are performed:

#. **constraints**: constraints on single fields are enforced, raising an error
    for each violation
#. **cross-constraints**: constraints involving multiple fields are enforced,
    raising an error for each violation
#. **defaults**: defaults are applied

Note
----

We currently chose not to use any default, in order to force the user to provide a
fully explicit input.
Even if in this way it will be a little bit more difficult to learn how to use
`yadism` it is not intended to be used by people not aware of its inputs.

Instead we are going to provide one or more example inputs in the project (or
project docs) and each field is fully described inside this subpackage in
:mod:`domains.yaml`.

The presence of `defaults.yaml` file is only to explicit our defaults' absence
and make the comparison with APFEL's ones.

"""
