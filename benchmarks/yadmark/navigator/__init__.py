import inspect

import IPython
from traitlets.config.loader import Config

from .navigator import NavigatorApp, t, o, l, compare_dicts


def yelp(*args):
    """
    Help function (renamed to avoid clash of names) - short cut: h.
    """
    if len(args) == 0:
        print(
            f"""Welcome to yadism benchmark skript!
Available variables:
    t = "{t}" -> query theories
    o = "{o}" -> query observables
    l = "{l}" -> query logs
Available functions:
    h() - this help
    m(str) - change mode
    g(tbl,id) - getter
    ls(tbl) - listing table with reduced informations
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


app = NavigatorApp("sandbox")


def m(*args):
    global app
    return app.change_mode(*args)


def g(*args):
    global app
    return app.get(*args)


def ls(*args):
    global app
    return app.list_all(*args)


def dfl(*args):
    global app
    return app.get_log_DFdict(*args)


def diff(*args):
    global app
    return app.subtract_tables(*args)


def truncate_logs():
    global app
    return app.logs.truncate()


def simlogs(*args):
    global app
    return app.list_all_sim_logs(*args)


def cmpt(id1, id2):
    return compare_dicts(g(t, id1), g(t, id2))


def check_dfdl(id_):
    dfd = dfl(id_)
    for n, df in dfd.items():
        for l in df.iloc:
            if abs(l["rel_err[%]"]) > 1 and abs(l["APFEL"] - l["yadism"]) > 1e-6:
                print(n, l, sep="\n")


def launch_navigator():
    c = Config()
    banner = """
        Welcome to yadism benchmark skript!
        call yelp() or h() for a brief overview.
    """
    c.TerminalInteractiveShell.banner2 = inspect.cleandoc(banner) + "\n" * 2

    init_cmds = ["""from yadmark.navigator import *""", """from yadism import *"""]
    args = ["--pylab"]
    for cmd in init_cmds:
        args.append(f"--InteractiveShellApp.exec_lines={cmd}")

    IPython.start_ipython(argv=args, config=c)
