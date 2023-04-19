import argparse
import pathlib

import banana
from banana import cfg as banana_cfg
from banana import navigator as bnav

from . import glob, navigator

here = pathlib.Path(__file__).parent
banana.register(here.parents[2] / "benchmarks")


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
    compare(id,id) - compare externals
    check_log(id) - check logs passed
    crashed_log(id) - print crashed logs
"""
        )
    elif len(args) == 1:
        return help(*args)
    return None


def register_globals(configpath):
    app = navigator.NavigatorApp(configpath, "sandbox")
    glob.app = app

    glob.glob["yelp"] = yelp
    glob.glob["h"] = yelp

    # register banana functions
    bnav.register_globals(glob.glob, glob.app)

    # add my functions
    glob.glob["check_log"] = app.check_log


def launch_navigator():
    """CLI Entry point"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config", type=pathlib.Path, default=None, help="Path to config file"
    )

    args = parser.parse_args()

    register_globals(banana_cfg.detect(args.config))

    return bnav.launch_navigator(
        ["yadism", "yadmark", "yadmark.navigator.glob"], skip_cfg=True
    )
