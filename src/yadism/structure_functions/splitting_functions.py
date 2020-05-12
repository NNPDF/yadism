# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""


def pqq_reg(x, constants):
    return -constants.CF * (1 + x)


def pqq_delta(x, constants):
    return (3 / 2) * constants.CF


def pqq_pd(x, constants):
    return 2 * constants.CF


def pqg(x, constants):
    return constants.TF * (x ** 2 + (1 - x) ** 2)
