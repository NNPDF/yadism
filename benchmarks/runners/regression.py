from pathlib import Path
import yaml
from yadmark.benchmark.runner import Runner
import lhapdf
import pandas as pd

REG_DIR = Path("regression")
REG_INP = REG_DIR / "regression_input.yaml"
BASELINE = REG_DIR / "baseline.yaml"
RES = REG_DIR / "current_result.yaml"

class Regression(Runner):

    def __init__(self):
        super().__init__()
        self.external = "void"
        self.run_tests()
        self.run_comparison()

    def _load_baseline(self):
        """
        Load the regression baseline
        """
        with open(BASELINE, "r") as f:
            self.baseline = yaml.safe_load(f)
  
    def _load_regression_inps(self):
        """
        Load the regression test inputs
        """
        with open(REG_INP, "r") as f:
            data = yaml.safe_load(f)
        return data

    def run_tests(self):
        """
        Run yadism on specified reggression inputs
        """
        data = self._load_regression_inps()
        results = {}
        for t, kws in data.items():
            kws["pdf"] = lhapdf.mkPDF(kws["pdf"])
            results[t] = self.run_me(**kws).get_raw()
        self.results = results
        with open(RES, "w") as f:
            yaml.dump(self.results, f)

    def update_baseline(self):
        """
        Update the numbers we compare the new results to.
        """
        with open(BASELINE, "w") as f:
            yaml.dump(self.results, f)

    def run_comparison(self):
        self._load_baseline()
        for test in self.results.keys():
            print(f"Comparison for {test}:")
            for obs in self.results[test]:
                print(f"Observable: {obs}")
                base = self.baseline[test][obs]
                new = self.baseline[test][obs]
                print_comparison(base, new)

def print_comparison(dict1, dict2):
    comp_table = pd.DataFrame(dict1)
    comp_table["baseline"] = comp_table["result"]
    comp_table["new value"] = pd.DataFrame(dict2)["result"]
    ## TODO make sure you handle division by 0 comp_table["difference [%]"] = (comp_table["new value"] - comp_table["baseline"]) / comp_table["baseline"]
    comp_table = comp_table[comp_table.columns.difference(["error", "result"])]
    print(comp_table)

if __name__ == "__main__":
    reg = Regression()
