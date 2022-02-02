from . import BCDMS, CHORUS, HERA, NMC, NUTEV, SLAC
from . import cli
from . import utils

exps = {
    getattr(m, "__name__").split(".")[-1]: m
    for m in [CHORUS, HERA, NMC, NUTEV, SLAC, BCDMS]
}


def main():
    args = cli.parse_cli()

    for i in args.inputs:
        path = utils.runcards.parent / i
        exp = exps[list(filter(lambda e: e in path.parent.name, exps.keys()))[0]]
        try:
            new_name = exp.new_names[path.stem]
        except KeyError:
            print(f"Skipped {path}")
            continue

        if isinstance(new_name, str):
            cli.dump(exp, path, new_name)
        else:
            for name in new_name:
                cli.dump(exp, path, name)
