# -*- coding: utf-8 -*-
# Installation script for python
from setuptools import find_packages, setup

setup(
    name="yadmark",
    author="F. Hekhorn, A.Candido",
    version="0.1.0",
    description="yadism benchmark",
    # package_dir={"": "."},
    packages=find_packages("."),
    install_requires=[
        "yadism",
        "rich",
        "sqlalchemy",
        "banana-hep",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "navigator=yadmark.navigator:launch_navigator",
        ],
    },
    python_requires=">=3.7",
)
