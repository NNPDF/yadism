# -*- coding: utf-8 -*-
import copy

import numpy as np
from banana.data import theories

import yadism
from yadmark.data import observables


def generate_theory():
    theory = copy.deepcopy(theories.default_card)

    return theory


def generate_observable():
    observable = copy.deepcopy(observables.default_card)

    kinematics = []
    kinematics.extend([dict(x=x, Q2=20.0, y=0) for x in np.geomspace(1e-4, 0.9, 10)])
    kinematics.extend(
        [dict(x=0.1, Q2=Q2, y=0) for Q2 in np.geomspace(4, 20, 10).tolist()]
    )

    return observable


def compute_sf():
    theory = generate_theory()
    observable = generate_observable()

    theory["TMC"] = 0

    return yadism.Runner(theory, observable).get_result()


def compute_sf_tmc():
    theory = generate_theory()
    observable = generate_observable()

    theory["TMC"] = 1

    return yadism.Runner(theory, observable).get_result()


class MemorySuite:
    def mem_sf(self):
        return compute_sf()

    def mem_sf_tmc(self):
        return compute_sf_tmc()


class PeakMemorySuite:
    def peakmem_sf(self):
        compute_sf()

    def peakmem_sf_tmc(self):
        compute_sf_tmc()


class TimeSuite:
    def time_sf(self):
        compute_sf()

    def time_sf_tmc(self):
        compute_sf_tmc()
