# -*- coding: utf-8 -*-
"""
Testing the input inspector, and the constraints
"""
import inspect

from yadism.input import Inspector, DomainError


def test_inspector(theory, observables):
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
        known_errors_names = [""]
        assert de.name in known_errors_names


def test_():
    pass


if __name__ == "__main__":
    test_dir = os.path.dirname(__file__)

    # read files
    theory_file = os.path.join(test_dir, "data/theory1.yaml")
    with open(theory_file, "r") as file:
        theory = yaml.safe_load(file)
    observables_file = os.path.join(test_dir, "data/dis_observables.yaml")
    with open(observables_file, "r") as file:
        dis_observables = yaml.safe_load(file)

    test_inspector(theory_file, observables_file)
