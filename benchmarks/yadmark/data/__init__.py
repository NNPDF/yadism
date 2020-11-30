# -*- coding: utf-8 -*-
import pathlib
import itertools

import yaml


def power_set(inp):
    """
    Thank you: https://stackoverflow.com/questions/5228158/
    """
    return [
        dict(zip(inp.keys(), values)) for values in itertools.product(*inp.values())
    ]


with open(pathlib.Path(__file__).parent / "pineappl_default_grid.yaml") as fd:
    pineappl_zgrid = yaml.safe_load(fd)
