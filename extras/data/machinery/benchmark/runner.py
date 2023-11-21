"""Benchmark yadism against apfel."""
import pathlib

dataroot = pathlib.Path(__file__).parents[2]


def benchmark(theory: dict, observables: dict, pdf: str):
    """Run a given benchmark against apfel."""
    # import banana and yadmark here to be able still to run generate outside
    # the environment
    from banana import register  # pylint: disable=import-outside-toplevel

    from yadmark.benchmark.runner import (  # pylint: disable=import-outside-toplevel
        Runner,
    )

    register(dataroot)

    runner = Runner()
    runner.external = "apfel"

    for obs, esfs in observables["observables"].items():
        observables["observables"][obs] = list(
            filter(lambda esf: esf["Q2"] > 1.0, esfs)
        )

    runner.run([theory], [observables], [pdf])
