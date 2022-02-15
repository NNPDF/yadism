# -*- coding: utf-8 -*-
import argparse

from .physics import scan


def configure():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--mc", action="store_true", help="FONLL for charm mass")
    parser.add_argument("-b", "--mb", action="store_true", help="FONLL for bottom mass")
    parser.add_argument("-t", "--mt", action="store_true", help="FONLL for top mass")

    parser.add_argument("-o", "--obs", default="total", help="Requested observable")

    parser.add_argument(
        "-i", "--intrinsic", nargs="+", type=int, help="Intrinsic flavors"
    )

    args = parser.parse_args()

    return args


def simulate():
    confs = configure()

    scan(confs).render()
