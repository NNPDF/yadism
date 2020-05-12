# Installation script for python
from setuptools import setup, find_packages

setup(
    name="yadism",
    version="0.0.1",
    description="Deep Inelastic Scattering",
    author="A.Candido, S.Carrazza, F. Hekhorn",
    author_email="stefano.carrazza@cern.ch",
    url="https://github.com/N3PDF/dis",
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={"": ["*.yaml"], "tests": ["*"]},
    zip_safe=False,
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        # resort true install dependencies and test/benchmark ones
        "eko",
        "numpy",
        "scipy",
        "pandas",
        "numba",
        "pyyaml>=5.1",
        # "pyyaml",
        # "tinydb~=4.1",
        # "human-dates2",
        # "sphinx",
        # "sphinx_rtd_theme",
        # "recommonmark",
        # "sphinxcontrib-bibtex",
    ],
    python_requires=">=3.7",
    # entry_points={"console_scripts": ["run-dis=yadism.runner:run_dis"],},
)
