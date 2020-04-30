import pathlib
import itertools

import yaml
import tinydb

# import numpy as np
here = pathlib.Path(__file__).parent.absolute()

db = tinydb.TinyDB(here / "input.json")
theories_table = db.table("theories")
# for the time being the table is freshly generated at each run of this script
theories_table.purge()

matrix = {
    "PTO": [0, 1],
    "XIR": [0.5, 1.0, 2.0],
    "XIF": [0.5, 1.0, 2.0],
    "PDFSet": ["ToyLH", "CT14llo_NF3", "uonly", "gonly"],
}


def my_product(inp):
    """
    Thank you: https://stackoverflow.com/questions/5228158/
    """
    return [
        dict(zip(inp.keys(), values)) for values in itertools.product(*inp.values())
    ]


with open(here / "theory_template.yaml") as f:
    template = yaml.safe_load(f)


for config in my_product(matrix):
    template.update(config)
    theories_table.insert(template)
