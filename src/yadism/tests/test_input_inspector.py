# -*- coding: utf-8 -*-
"""
Testing the input inspector, and the constraints
"""
import inspect
import os

import yaml

from yadism.input.inspector import Inspector, DomainError
from yadism.tests.aux.file_loader import FileLoader


def test_inspector():
    fl = FileLoader()

    observables = fl.load_yaml("dis_observables.yaml")

    # FNS -> example of `enum` type argument
    # polDIS -> example of 'real' type argument
    theories = {"FNS": "theory_input_fns.yaml", "polDIS": "theory_input_poldis.yaml"}

    for known_error_name, theory_file in theories.items():
        theory = fl.load_yaml(theory_file)
        insp = Inspector(theory)
        try:
            insp.check_domains()
            # I'm giving him a wrong theory
            # so if does not raise any error... is an error
            msg = inspect.cleandoc(
                """test_inspector: check_domains does not notice known
                DomainErrors"""
            )
            assert False, msg
        except DomainError as de:
            assert de.name == known_error_name


def test_():
    pass


if __name__ == "__main__":
    test_inspector()
