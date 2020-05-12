import pathlib
import sys
from datetime import datetime

import tinydb
import numpy as np

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from apfel_utils import (
    str_datetime,
)  # pylint:disable=import-error,wrong-import-position

db = tinydb.TinyDB(here / "input.json")
obs_table = db.table("observables")
# for the time being the table is freshly generated at each run of this script
obs_table.truncate()

observables = [
    "F2light",
    "F2charm",
    "F2bottom",
    "F2top",
    "FLlight",
    "FLcharm",
    "FLbottom",
    "FLtop",
]

# keep in mind, that in TMC xi < x
xgrid = np.unique(np.concatenate([np.logspace(-4, -1, 20), np.linspace(0.1, 0.99, 10)]))
polynomial_degree = 4
is_log_interpolation = True

kinematics = []
# fixed Q
kinematics.extend([dict(x=x, Q2=90.0) for x in np.logspace(-3, -1, 6).tolist()])
kinematics.extend([dict(x=x, Q2=90.0) for x in np.linspace(0.15, 0.9, 6).tolist()])
# fixed x
kinematics.extend([dict(x=0.8, Q2=Q2) for Q2 in np.logspace(1.5, 2.5, 6).tolist()])

# iterate over observables (one dict for each)
for sf in observables:
    content = dict(
        xgrid=xgrid.tolist(),
        polynomial_degree=polynomial_degree,
        is_log_interpolation=is_log_interpolation,
        prDIS="NC",
        comments="",
        _modify_time=str_datetime(datetime.now()),
    )
    content[sf] = kinematics

    obs_table.insert(content)
