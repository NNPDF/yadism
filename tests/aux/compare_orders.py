import sys
import os

import pandas as pd

sys.path.append(os.path.dirname(__file__))
from utils import logs_dir


def subtract_tables(file1, file2, output_f):
    table1 = pd.read_csv(file1, index_col=0)
    table2 = pd.read_csv(file2, index_col=0)

    if any([any(table1[y] != table2[y]) for y in ["x", "Q2"]]):
        raise ValueError("Cannot compare tables with different (x, Q2)")

    table2["APFEL"] -= table1["APFEL"]
    table2["yadism"] -= table1["yadism"]
    table2["yadism_error"] += table1["yadism_error"]

    def rel_err(row):
        ref = row["APFEL"]
        fx = row["yadism"]
        if ref == 0.0:
            comparison = np.nan
        else:
            comparison = (fx / ref - 1.0) * 100
        return comparison

    # table2.drop(["rel_err[%]"], inplace=True)
    table2["rel_err[%]"] = table2.apply(rel_err, axis=1)
    with open(output_f, "w") as f:
        table2.to_csv(f)


if __name__ == "__main__":
    F2light_LO = logs_dir / "theory_LO-F2light-F2light.csv"
    F2light_NLO = logs_dir / "theory_NLO-F2light-F2light.csv"
    output_f = logs_dir / "theory_pNLO-F2light-F2light.csv"
    subtract_tables(F2light_NLO, F2light_LO, output_f)
