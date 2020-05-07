# -*- coding: utf-8 -*-
"""
Provides splitting functions definition for coefficient functions calculation.

The coefficient functions are defined in ???, and they are organized in:

- qq
- qg
- gq
- gg

according to the partons (entering the hard process - coming from the proton).

Furthermore they are organized according to their distribution structure, for
which see :py:mod:`convolution`.

.. todo::
    - Reference: pink book
"""


def pqq_reg(x, constants):
    return -constants.CF * (1 + x)


def pqq_delta(x, constants):
    return (3 / 2) * constants.CF


def pqq_pd(x, constants):
    return 2 * constants.CF


def pqg(x, constants):
    return constants.TF * (x ** 2 + (1 - x) ** 2)
