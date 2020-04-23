import sys
import os

import pandas as pd

sys.path.append(os.path.dirname(__file__))
from utils import logs_dir


def subtract_tables(file1, file2, output_f):
    """
        Subtract yadism and APFEL result in the second table from the first one,
        properly propagate the integration error and recompute the relative
        error on the subtracted results.

        Parameters
        ----------
        file1 :
            path for csv file with the table to subtract from
        file2 :
            path for csv file with the table to be subtracted
        output_f :
            path for csv file to store the result
    """
    # load tables
    table1 = pd.read_csv(file1, index_col=0)
    table2 = pd.read_csv(file2, index_col=0)

    # check for compatible kinematics
    if any([any(table1[y] != table2[y]) for y in ["x", "Q2"]]):
        raise ValueError("Cannot compare tables with different (x, Q2)")

    # subtract and propagate
    table2["APFEL"] -= table1["APFEL"]
    table2["yadism"] -= table1["yadism"]
    table2["yadism_error"] += table1["yadism_error"]

    # compute relative error
    def rel_err(row):
        if row["APFEL"] == 0.0:
            return np.nan
        else:
            return (row["yadism"] / row["APFEL"] - 1.0) * 100

    table2["rel_err[%]"] = table2.apply(rel_err, axis=1)

    # dump results' table
    with open(output_f, "w") as f:
        table2.to_csv(f)
    print(table2)


if __name__ == "__main__":
    # hard coded paths
    # F2light_LO = logs_dir / "theory_LO-F2light-F2light.csv"
    # F2light_NLO = logs_dir / "theory_NLO-F2light-F2light.csv"
    # output_f = logs_dir / "theory_pNLO-F2light-F2light.csv"

    # run subtraction
    # subtract_tables(F2light_NLO, F2light_LO, output_f)

    F2light_NLO = logs_dir / "theory_NLO-F2light-F2light.csv"
    F2light_NLO_SV = logs_dir / "theory_SV_NLO-F2light-F2light.csv"
    output_f = logs_dir / "theory_pSV_NLO-F2light-F2light.csv"

    # run subtraction
    subtract_tables(F2light_NLO_SV, F2light_NLO, output_f)
