# -*- coding: utf-8 -*-
from banana.data import theories
from .. import banana_cfg
from . import observables

generate_theories = theories.TheoriesGenerator.get_run_parser(banana_cfg.banana_cfg)

generate_observables = observables.ObservablesGenerator.get_run_parser(
    banana_cfg.banana_cfg
)
