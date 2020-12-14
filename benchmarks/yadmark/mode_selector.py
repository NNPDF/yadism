# -*- coding: utf-8 -*-
import pathlib

import tinydb

here = pathlib.Path().parent.absolute()


class ModeSelector:
    """
    Handle the mode-related stuff

    Parameters
    ----------
        mode : str
            active mode
        external : str
            external program name to compare to if in sandbox mode
    """

    def __init__(self, mode, external=None):
        self.mode = mode
        if mode == "sandbox":
            self.external = external
        else:
            if external is not None and mode != external:
                raise ValueError(f"in {mode} mode you have {mode} as external")
            self.external = mode
        self.data_dir = here.parent / "data"
        # load DBs
        self.input_name = self.get_input_name()
        self.idb = tinydb.TinyDB(self.data_dir / self.input_name)
        self.odb = tinydb.TinyDB(self.data_dir / "output.json")

    def get_input_name(self):
        """Determine DB name"""
        if self.mode == "regression":
            return "regression.json"
        if self.mode == "APFEL":
            return "apfel-input.json"
        if self.mode == "QCDNUM":
            return "qcdnum-input.json"
        if self.mode == "FONLLdis":
            return "fonlldis-input.json"
        # sandbox
        return "input.json"
