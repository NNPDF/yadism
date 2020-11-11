# -*- coding: utf-8 -*-
from banana import navigator as bnav
from yadism import observable_name as on

from .. import banana_cfg
from . import navigator


def yelp(*args):
    """
    Help function (renamed to avoid clash of names) - short cut: h.
    """
    if len(args) == 0:
        print(
            f"""Welcome to yadism benchmark skript!
Available variables:
    {bnav.help_vars}
    o = "{bnav.o}" -> query observables
Available functions:
    {bnav.help_fncs}
    dfl(id) - log as DataFrame
    diff(id,id) - subtractig logs
    truncate_logs() - clear log table
    simlogs(id) - find similar logs
"""
        )
    elif len(args) == 1:
        return help(*args)
    return None


h = yelp

app = navigator.NavigatorApp(banana_cfg.banana_cfg,"sandbox")

bnav.register_globals(globals(), app)


# def dfl(*args):
#     global app
#     return app.get_log_DFdict(*args)


# def diff(*args):
#     global app
#     return app.subtract_tables(*args)


# def simlogs(*args):
#     global app
#     return app.list_all_sim_logs(*args)


# def check_dfdl(id_):
#     dfd = dfl(id_)
#     for n, df in dfd.items():
#         for l in df.iloc:
#             if abs(l["rel_err[%]"]) > 1 and abs(l["APFEL"] - l["yadism"]) > 1e-6:
#                 print(n, l, sep="\n")

# def crashedfl(id_):
#     dfd = g(l, id_)
#     if "_crash" not in dfd:
#         raise ValueError("log didn't crash!")
#     cdfd = {}
#     for sf in dfd:
#         if on.ObservableName.is_valid(sf):
#             cdfd[sf] = f"{len(dfd[sf])} points"
#         else:
#             cdfd[sf] = dfd[sf]
#     return cdfd


def launch_navigator():
    return bnav.launch_navigator("yadism", "yadmark")
