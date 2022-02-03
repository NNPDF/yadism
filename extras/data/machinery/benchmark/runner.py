# -*- coding: utf-8 -*-
import pathlib

dataroot = pathlib.Path(__file__).parents[2]


def benchmark(theory, observables):
    # import banana and yadmark here to be able still to run generate outside
    # the environment
    from banana import register

    from yadmark.benchmark.runner import Runner

    register(dataroot)

    runner = Runner()
    runner.external = "apfel"

    runner.run([theory], [observables], ["ToyLH"])
