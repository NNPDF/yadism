# -*- coding: utf-8 -*-
# Installation script for python
from setuptools import setup, find_packages

setup(
    name="yadmark",
    author="",
    version="0.1.0",
    description="yadism benchmark",
    # package_dir={"": "."},
    packages=find_packages("."),
    entry_points={
        "console_scripts": [
            "generate_theories=yadmark.data.theories:run_parser",
            "generate_observables=yadmark.data.observables:run_parser",
            "navigator=yadmark.navigator:launch_navigator",
        ],
    },
)
