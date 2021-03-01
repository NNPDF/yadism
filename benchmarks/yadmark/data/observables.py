# -*- coding: utf-8 -*-
import numpy as np

from eko import interpolation
from banana.data import cartesian_product, sql

from . import db

default_card = dict(
    interpolation_xgrid=interpolation.make_grid(30, 20).tolist(),
    interpolation_polynomial_degree=4,
    interpolation_is_log=True,
    prDIS="EM",
    ProjectileDIS="electron",
    PolarizationDIS=0,
    PropagatorCorrection=0,
    observables={},
)
default_card = dict(sorted(default_card.items()))

default_kinematics = []
default_kinematics.extend(
    [dict(x=x, Q2=10.0) for x in default_card["interpolation_xgrid"][3::3]]
)
default_kinematics.extend(
    [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 22, 10).tolist()]
)

default_config = {
    0: {"observable_names": ["F2light"], "kinematics": default_kinematics},
    1: {
        "observable_names": [
            "F2light",
            "F2charm",
            "FLlight",
            "FLcharm",
            "F3light",
            "F3charm",
        ],
        "kinematics": default_kinematics,
    },
}

fns_config = {
    "ZM-VFNS": {
        "observable_names": ["F2light", "FLlight", "F3light"],
        "kinematics": default_kinematics,
    }
}


def build(observable_names, kinematics, update=None):
    """
    Generate all observable card updates

    Parameters
    ----------
        observable_names : list(str)
            observable names
        kinematics : list(dict)
            kinematics list
        update : dict
            base modifiers

    Returns
    -------
        cards : list(dict)
            list of update
    """
    cards = []
    if update is None:
        update = {}
    for c in cartesian_product(update):
        card = dict(observables={})
        card.update(c)
        for obs in observable_names:
            card["observables"][obs] = kinematics
        cards.append(card)
    return cards


# db interface
def load(session, updates):
    """
    Load observable records from the DB.

    Parameters
    ----------
        session : sqlalchemy.session.Session
            DB ORM session
        updates : dict
            modifiers

    Returns
    -------
        cards : list(dict)
            list of records
    """
    # add hash
    raw_records, df = sql.prepare_records(default_card, updates)
    # insert new ones
    sql.insertnew(session, db.Observable, df)
    return raw_records
