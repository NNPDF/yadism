import numpy as np

from .. import partonic_channel as pc


class PartonicChannelHeavy(pc.PartonicChannel):
    """
    Heavy partonic coefficient functions that respect hadronic and partonic
    thresholds.
    """

    def __init__(self, *args, m2hq):
        self.m2hq = m2hq
        super().__init__(*args)
        # FH - Vogt comparison prefactor
        self._FHprefactor = self.ESF.Q2 / (np.pi * m2hq)

        # common variables
        self._rho_q = -4 * m2hq / self.ESF.Q2
        self._rho = lambda z: -self._rho_q * z / (1 - z)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

    def decorator(self, f):
        """
        Apply hadronic threshold

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        if self.is_below_threshold(self.ESF.x):
            return lambda: 0
        return f

    def is_below_threshold(self, z):
        """
        Checks if the available energy is below production threshold or not

        Parameters
        ----------
            z : float
                partonic momentum fraction

        Returns
        -------
            is_below_threshold : bool
                is the partonic energy sufficient to create the heavy quark
                pair?

        .. todo::
            use threshold on shat or using FH's zmax?
        """
        # import pdb; pdb.set_trace()
        shat = self.ESF.Q2 * (1 - z) / z
        return shat <= 4 * self.m2hq
