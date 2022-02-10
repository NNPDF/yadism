# -*- coding: utf-8 -*-
import IPython

cmds = """
import banana
banana.register(".")
from yadmark.navigator import *
"""

args = ["--pylab"]
for cmd in cmds.splitlines():
    args.append(f"--InteractiveShellApp.exec_lines={cmd}")


IPython.start_ipython(args)
