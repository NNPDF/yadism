# -*- coding: utf-8 -*-
import numpy as np

from eko import interpolation

from banana.data import power_set, sql

default_card = dict(
    interpolation_xgrid=interpolation.make_grid(30, 20).tolist(),
    interpolation_polynomial_degree=4,
    interpolation_is_log=True,
    prDIS="EM",
    projectile="electron",
    PolarizationDIS=0,
    observables={},
)
default_card = dict(sorted(default_card.items()))

default_kinematics = []
default_kinematics.extend(
    [dict(x=x, Q2=90.0) for x in default_card["interpolation_xgrid"][3::3]]
)
default_kinematics.extend(
    [dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()]
)

default_config = {
    0: {"observables": ["F2light"], "kinematics": default_kinematics},
    1: {
        "observables": ["F2light", "F2total", "FLtotal", "F3total"],
        "kinematics": default_kinematics,
    },
}


def build(observables, kinematics, update=None):
    """
    Generate all observable card updates

    Parameters
    ----------
        observables : list(str)
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
    for c in power_set(update):
        card = dict(observables={})
        card.update(c)
        for obs in observables:
            card["observables"][obs] = kinematics
            cards.append(card)
    return cards


# db interface
def load(conn, updates):
    raw_records, records, fields = sql.prepare_records(default_card, updates)
    sql.insert(conn, "observables", fields, records)
    return raw_records


# def regression_cards(defaults):
#     """
#     Collect regression run cards

#     Parameters
#     ----------
#         defaults : dict
#             default setup

#     Returns
#     -------
#         cards : list(dict)
#             list of cards
#     """
#     # only use a single card
#     cards = []
#     # iterate all options
#     matrix = dict(
#         prDIS=["EM", "NC", "CC"],
#         projectile=["electron", "positron", "neutrino", "antineutrino"],
#         PolarizationDIS=[0, 0.6],
#     )
#     for cfg in power_set(matrix):
#         reg = copy.deepcopy(defaults)
#         reg.update(cfg)
#         reg["F2light"] = [dict(x=0.01, Q2=90), dict(x=0.8, Q2=190)]
#         reg["FLlight"] = [dict(x=0.1, Q2=190)]
#         reg["F3light"] = [dict(x=0.1, Q2=190)]
#         for kind in ["F2", "FL", "F3"]:
#             reg[f"{kind}charm"] = [dict(x=0.01, Q2=50)]
#             reg[f"{kind}bottom"] = [dict(x=0.01, Q2=100)]
#             reg[f"{kind}top"] = [dict(x=0.01, Q2=1000)]
#             reg[f"{kind}total"] = [dict(x=0.01, Q2=90)]
#         cards.append(reg)
#     return cards


# def external_cards_qcdnum(defaults):
#     """
#     Collect QCDNUM run cards

#     Parameters
#     ----------
#         defaults : dict
#             default setup

#     Returns
#     -------
#         cards : list(dict)
#             list of cards
#     """
#     # fixed Q2 and fixed x
#     light_kin = []
#     light_kin.extend(
#         [dict(x=x, Q2=90.0) for x in defaults["interpolation_xgrid"][3::3]]
#     )
#     light_kin.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
#     cards = []
#     # LO runcard - only F2light is non-zero
#     lo_card = copy.deepcopy(defaults)
#     lo_card["PTO"] = 0
#     lo_card["F2light"] = copy.copy(light_kin)
#     cards.append(lo_card)
#     # NLO runcard
#     nlo_card = copy.deepcopy(defaults)
#     nlo_card["PTO"] = 1
#     obs_lists = [
#         ["F2light", "FLlight"],  # in ZM-VFNS only lights are available
#         [  # in FFNS3 all are available
#             "F2light",
#             "F2charm",
#             "F2bottom",
#             "F2top",
#             "FLlight",
#             "FLcharm",
#             "FLbottom",
#             "FLtop",
#         ],
#         [  # in FFNS4 all above bottom are available
#             "F2bottom",
#             "F2top",
#             "FLbottom",
#             "FLtop",
#         ],
#         ["F2top", "FLtop"],  # in FFNS5 only top is available
#     ]
#     for obs_list in obs_lists:
#         c = copy.deepcopy(nlo_card)
#         for obs in obs_list:
#             c[obs] = copy.copy(light_kin)  # for now take same kinematics
#         cards.append(c)
#     return cards


# def external_cards_apfel(defaults):
#     """
#     Collect APFEL run cards

#     Parameters
#     ----------
#         defaults : dict
#             default setup

#     Returns
#     -------
#         cards : list(dict)
#             list of cards
#     """
#     # fixed Q2 and fixed x
#     light_kin = []
#     light_kin.extend(
#         [dict(x=x, Q2=90.0) for x in defaults["interpolation_xgrid"][3::3]]
#     )
#     light_kin.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
#     # LO runcard - only F2light is non-zero
#     lo_card = copy.deepcopy(defaults)
#     lo_card["PTO"] = 0
#     lo_card["F2light"] = copy.copy(light_kin)
#     # NLO runcard
#     nlo_card = copy.deepcopy(defaults)
#     nlo_card["PTO"] = 1
#     obs_list = [
#         "F2light",
#         "F2charm",
#         "F2bottom",
#         "F2top",
#         "F2total",
#         "FLlight",
#         "FLcharm",
#         "FLbottom",
#         "FLtop",
#         "FLtotal",
#         "F3light",
#         "F3charm",
#         "F3bottom",
#         "F3top",
#         "F3total",
#     ]
#     for obs in obs_list:
#         nlo_card[obs] = copy.copy(light_kin)  # for now take same kinematics
#     cards = []
#     # now iterate meta, such as currents, etc.
#     matrix = dict(
#         prDIS=["EM", "NC", "CC"],
#         projectile=["electron", "positron", "neutrino", "antineutrino"],
#         PolarizationDIS=[0, 0.6],
#     )
#     for cfg in power_set(matrix):
#         for c in [lo_card, nlo_card]:
#             c.update(cfg)
#             cards.append(copy.copy(c))
#     return cards


# class ObservablesGenerator(CardGenerator):

#     table_name = "observables"

#     def get_all(self):
#         defaults = dict(
#             interpolation_xgrid=interpolation.make_grid(30, 20).tolist(),
#             interpolation_polynomial_degree=4,
#             interpolation_is_log=True,
#             prDIS="EM",
#             projectile="electron",
#             PolarizationDIS=0,
#         )
#         cards = []
#         # use only a small set in regression
#         if self.mode == "regression":
#             cards.extend(regression_cards(defaults))
#         elif self.mode == "APFEL":
#             cards.extend(external_cards_apfel(defaults))
#         elif self.mode == "QCDNUM":
#             cards.extend(external_cards_qcdnum(defaults))
#         elif self.mode == "sandbox":
#             # sandbox -> don't do anything; its cards are managed there
#             cards.extend([copy.deepcopy(defaults)])
#         return cards
