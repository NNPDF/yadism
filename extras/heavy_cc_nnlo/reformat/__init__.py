import argparse
import logging
import pathlib

from . import generate as gen
from . import parse

_logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("paths", nargs="*", type=pathlib.Path)
    parser.add_argument("-a", "--actions", nargs="*", choices=["dump", "plot"])

    return parser.parse_args()


def main():
    args = parse_args()

    for path in args.paths:
        ch, blocks = parse.parse(path)
        ds = gen.to_xarray(blocks)

        if "dump" in args.actions:
            dumpdest = pathlib.Path.cwd() / "data" / f"{path.stem}.nc"
            dumpdest.parent.mkdir(exist_ok=True)
            ds.to_netcdf(dumpdest)

            _logger.info(
                f"Saved xgrid array to {dumpdest.relative_to(pathlib.Path.cwd())}"
            )

        if "plot" in args.actions:
            dest = pathlib.Path.cwd() / "plots" / f"{path.stem}.png"
            dest.parent.mkdir(exist_ok=True)
            gen.plot(ds, dest)
