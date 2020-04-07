import pandas as pd


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
