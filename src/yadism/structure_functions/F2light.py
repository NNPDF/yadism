# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.

.. todo::
    docs
"""

import numpy as np

from .EvaluatedStructureFunction import EvaluatedStructureFunction as ESF
from . import splitting_functions as split


class ESF_F2light(ESF):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        super(ESF_F2light, self).__init__(SF, kinematics)

    def quark_0(self) -> float:
        """Computes the singlet part of the leading order F2 structure function.

        Implements equation 4.2 of :cite:`Vermaseren:2005qc`.

        Parameters
        ----------
        x : float
            Bjorken x
        Q2 : float
            squared(!) momentum transfer

        Returns
        -------
        float
            F2(x,Q^2)

        .. todo::
            docs
        """

        # leading order is just a delta function
        return lambda z: 0, lambda z: 1

    def gluon_0(self) -> float:
        """
        .. todo::
            docs
        """
        return 0

    def quark_1(self):
        """
        regular
        delta
        1/(1-x)_+
        log(x)/(1-x)_+

        .. todo::
            docs
        """
        CF = self._SF._constants.CF
        zeta_2 = np.pi ** 2 / 6

        def cq_reg(z):
            # fmt: off
            return CF*(
                - 2 * (1 + z) * np.log((1 - z) / z)
                - 4 * np.log(z) / (1 - z)
                + 6 + 4 * z
            )
            # fmt: on

        def cq_delta(z):
            return -CF * (9 + 4 * zeta_2)

        def cq_omx(z):
            return -3 * CF

        def cq_logomx(z):
            return 4 * CF

        return cq_reg, cq_delta, cq_omx, cq_logomx

    def gluon_1(self):
        """
        vogt page 21

        .. todo::
            docs
        """

        TR = self._SF._constants.TF

        def cg(z):
            return (
                2
                * self._n_f
                * (
                    split.pqg(z, self._SF._constants) * (np.log((1 - z) / z) - 4)
                    + 3 * TR
                )
            )

        return cg
