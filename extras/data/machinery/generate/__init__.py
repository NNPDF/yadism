# -*- coding: utf-8 -*-
import argparse

from . import BCDMS, CHORUS, HERA, NMC, NUTEV, SLAC, utils

exps = {
    getattr(m, "__name__").split(".")[-1]: m
    for m in [CHORUS, HERA, NMC, NUTEV, SLAC, BCDMS]
}


def cli(subparsers):
    ap = subparsers.add_parser(
        "generate",
        description=f"""
            runcards generator: generate 'observable.yaml' from names
            and commondata files (output stored in '{utils.runcards}')""",
    )
    ap.add_argument(
        "inputs",
        nargs="+",
        help="path inside an EXPERIMENT folder (e.g. 'CHORUSPb/x-sec_shift_nb.txt')",
    )
    ap.set_defaults(func=main)


def main(args):
    for i in args.inputs:
        path = utils.runcards.parent / i
        exp = exps[list(filter(lambda e: e in path.parent.name, exps.keys()))[0]]
        try:
            new_name = exp.new_names[path.stem]
        except KeyError:
            print(f"Skipped {path}")
            continue

        if isinstance(new_name, str):
            utils.dump(exp, path, new_name)
        else:
            for name in new_name:
                utils.dump(exp, path, name)
