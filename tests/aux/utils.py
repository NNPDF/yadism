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


logs_dir = test_data_dir / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)


def print_comparison_table(res_tab, log_path_template=None):

    for FX, tab in res_tab.items():
        if len(tab) == 0:
            continue
        print_tab = pd.DataFrame(tab)

        # print results
        print(f"\n---{FX}---\n")
        print(print_tab)
        print("\n--------\n")

        if log_path_template is not None:
            log_path = log_path_template.parent / log_path_template.name.format(obs=FX)
            with open(log_path, "w") as f:
                print_tab.to_csv(f)
