# -*- coding: utf-8 -*-
from banana import navigator as bnav

from .. import banana_cfg
from . import navigator


def yelp(*args):
    """
    Help function (renamed to avoid clash of names) - short cut: h.
    """
    if len(args) == 0:
        print(
            f"""Welcome to yadmark navigator - the yadism benchmark skript!
Available variables:
    {bnav.help_vars}
    o = "{bnav.o}" -> query observables
Available functions:
    {bnav.help_fncs}
    dfl(id) - log as DataFrame
    simlogs(id) - find similar logs
    diff(id,id) - subtractig logs
    check_log(id) - check logs passed
    crashed_log(id) - print crashed logs
"""
        )
    elif len(args) == 1:
        return help(*args)
    return None


h = yelp

app = navigator.NavigatorApp(banana_cfg.banana_cfg, "sandbox")

# register banana functions
bnav.register_globals(globals(), app)

# add my functions
dfl = app.log_as_DFdict
simlogs = app.list_all_sim_logs
diff = app.subtract_tables
check_log = app.check_log
crashed_log = app.crashed_log


def launch_navigator():
    return bnav.launch_navigator("yadism", "yadmark")
