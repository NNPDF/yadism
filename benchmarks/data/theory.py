import pathlib
import itertools
import sys
from datetime import datetime

import yaml
import tinydb

# import numpy as np
here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from apfel_utils import str_datetime  # pylint:disable=import-error

db = tinydb.TinyDB(here / "input.json")
theories_table = db.table("theories")
# for the time being the table is freshly generated at each run of this script
theories_table.purge()

matrix = {
    "PTO": [0, 1],
    "XIR": [0.5, 1.0, 2.0],
    "XIF": [0.5, 1.0, 2.0],
    "TMC": [0, 1],
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
    template["_modify_time"] = str_datetime(datetime.now())
    theories_table.insert(template)
