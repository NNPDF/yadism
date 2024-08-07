from . import (
    BCDMS,
    CHORUS,
    COMPASS15,
    E142,
    E143,
    E154,
    E155,
    EMC,
    HERA,
    HERMES,
    HERMES97,
    JLABE06,
    JLABE97,
    JLABE99,
    JLABEG1B,
    JLABEG1DVCS,
    NMC,
    NUTEV,
    POS,
    SLAC,
    SMC,
    SMCSX,
    utils,
)

exps = {
    getattr(m, "__name__").rsplit(".", maxsplit=1)[-1]: m
    for m in [
        BCDMS,
        CHORUS,
        E142,
        E143,
        E154,
        E155,
        EMC,
        SMC,
        SMCSX,
        COMPASS15,
        HERMES,
        HERMES97,
        JLABE06,
        JLABE97,
        JLABE99,
        JLABEG1B,
        JLABEG1DVCS,
        HERA,
        NMC,
        NUTEV,
        POS,
        SLAC,
    ]
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
        exp = exps[
            list(filter(lambda e, path=path: e == path.parent.name, exps.keys()))[0]
        ]
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
