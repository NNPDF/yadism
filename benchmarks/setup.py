# -*- coding: utf-8 -*-
# Installation script for python
from setuptools import setup, find_packages

setup(
    name="yadmark",
    author="F. Hekhorn, A.Candido",
    version="0.1.0",
    description="yadism benchmark",
    # package_dir={"": "."},
    packages=find_packages("."),
    install_requires=[
        "rich",
        "banana-hep",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "generate_theories=yadmark.data:generate_theories",
            "generate_observables=yadmark.data:generate_observables",
            "navigator=yadmark.navigator:launch_navigator",
        ],
    },
    python_requires=">=3.7",
)
