import pathlib

import yaml
import pandas as pd

test_data_dir = pathlib.Path(__file__).absolute().parents[1] / "data"


def load_runcards(theory_file, observables_file):
    """Test the loading mechanism"""

    # read files
    # theory
    with open(theory_file, "r") as f:
        theory = yaml.safe_load(f)

    # observables
    with open(observables_file, "r") as f:
        dis_observables = yaml.safe_load(f)

    return theory, dis_observables


def print_comparison_table(res_tab):

    for FX, tab in res_tab.items():
        if len(tab) == 0:
            continue
        print_tab = pd.DataFrame(tab)
        # print_tab.columns = ["x", "Q2", "APFEL", "yadism", "yadism_error", "rel_err[%]"]

        # print results
        print(f"\n---{FX}---\n")
        print(print_tab)
        print("\n--------\n")
