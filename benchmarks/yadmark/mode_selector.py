# -*- coding: utf-8 -*-

from banana import mode_selector
from . import banana_cfg


class ModeSelector(mode_selector.ModeSelector):
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
        super().__init__(banana_cfg.banana_cfg, mode)
        self.external = external
