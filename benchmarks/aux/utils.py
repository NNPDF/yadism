import pathlib

import yaml
import pandas as pd

# define data and logs dirs used by tests
test_data_dir = pathlib.Path(__file__).absolute().parents[1] / "data"
logs_dir = test_data_dir / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)


def load_runcards(theory_file, observables_file):
    """
       Load runcards from ``yaml`` files.

        Parameters
        ----------
        theory_file :
            path to yaml theory runcard
        observables_file :
            path to yaml observables runcard

        Returns
        -------
        dict
            loaded theory dict
        dict
            loaded observables dict
    """

    # read files
    # theory
    with open(theory_file, "r") as f:
        theory = yaml.safe_load(f)

    # observables
    with open(observables_file, "r") as f:
        dis_observables = yaml.safe_load(f)

    return theory, dis_observables


def print_comparison_table(res_tab, log_path_template=None):
    """
        Print and dump comparison table.

        Parameters
        ----------
        res_tab :
            dict of lists of dicts, to be printed and saved in multiple csv
            files
        log_path_template :
            path template for file where dumping res_tab (default: None)
    """

    # for each observable:
    for FX, tab in res_tab.items():
        if len(tab) == 0:
            continue
        print_tab = pd.DataFrame(tab)

        # print results
        print(f"\n---{FX}---\n")
        print(print_tab)
        print("\n--------\n")

        # if path available also save on file
        if log_path_template is not None:
            log_path = log_path_template.parent / log_path_template.name.format(obs=FX)
            with open(log_path, "w") as f:
                print_tab.to_csv(f)


def get_package_modules(package_path):
    modules = pathlib.Path(package_path).glob("**/*.py")
    return modules


def get_most_recent_timestamp(paths):
    most_recent = max([p.stat().st_mtime for p in paths])

    return most_recent
