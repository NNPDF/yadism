# -*- coding: utf-8 -*-
"""
File loader for tests:
    * knows the path of test data files
    * knows the methods to load different data types
    * keeps a cache of loaded files
"""

import os

import yaml


class FileLoader:
    """File loader with a cache.

    It's almost a singleton: not all the instances are the same one but they
    share all the relevant attributes.

    Attributes
    ----------
    cache : dict
        Cache of the loaded files, saved as dict with file names as keys.
    test_data_dir : str
        Path to directory with data for tests.

    """

    cache = {}
    test_data_dir = None

    @classmethod
    def __init__(cls):
        """Build the actual path to tests' data, only once."""
        if not cls.test_data_dir:
            cls.test_data_dir = os.path.join(os.path.dirname(__file__), "../data")

    @classmethod
    def load_yaml(cls, file_name):
        """Load yaml files.

        Parameters
        ----------
        cls :
            The object's class.
        file_name : str
            The name of the file requested (name only, not the full nor relative
            path, it will be searched in tests data dir).

        Returns
        -------
        dict
            File content.

        """
        file_path = os.path.join(cls.test_data_dir, file_name)

        if file_name not in cls.cache.keys():
            with open(file_path, "r") as file:
                file_content = yaml.safe_load(file)

            cls.cache[file_name] = file_content
        else:
            file_content = cls.cache[file_name]

        return file_content
