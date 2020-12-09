# -*- coding: utf-8 -*-

import numpy as np

from ..partonic_channel import PartonicChannelHeavyIntrinsic


class F2IntrinsicSp(PartonicChannelHeavyIntrinsic):
    def LO(self):
        factor = self.delta / self.ESF.Q2 * self.ESF.x / self.convolution_point()
        return 0, 0, factor

    def NLO(self):
        def reg(z):
            self.init_vars(z)
            return self.fhat()

        return reg

    def fhat(self):
        return (
            -8
            * (
                4
                * self.delta ** 4
                * (self.m2sq + self.s1hat)
                * (1 + self.I_xi * self.s1hat)
                + self.s1hat
                * (
                    2
                    * (self.m2sq + self.s1hat)
                    * (
                        self.m2sq
                        * (
                            2 * self.s1hat ** 2
                            + 10 * self.s1hat * self.sigma_pm
                            + 9 * self.sigma_pm ** 2
                        )
                        - 2
                        * self.m1sq
                        * (
                            6 * self.m2sq * self.ESF.Q2
                            + self.s1hat
                            * (6 * self.ESF.Q2 - self.s1hat + self.sigma_pm)
                        )
                    )
                    + self.s1hat
                    * (-self.deltap ** 2 + 6 * self.ESF.Q2 * (self.m2sq + self.s1hat))
                    * self.sigma_pp
                    + (-self.deltap ** 2 + 6 * self.ESF.Q2 * (self.m2sq + self.s1hat))
                    * self.sigma_pp ** 2
                )
                + 2
                * self.delta ** 2
                * (self.m2sq + self.s1hat)
                * (
                    self.m2sq * (3 * self.s1hat + 8 * self.sigma_pm)
                    - 2 * self.s1hat * (self.s1hat - 2 * self.sigma_pm + self.sigma_pp)
                )
            )
        ) / (self.deltap ** 4 * self.s1hat * (self.m2sq + self.s1hat)) - (
            16
            * self.L_xi
            * (self.m2sq + self.s1hat)
            * (
                2 * self.delta ** 4
                + 2
                * self.delta ** 2
                * (self.s1hat + 2 * self.sigma_pm)
                * (self.s1hat + self.sigma_pp)
                + self.s1hat
                * (
                    self.deltap ** 2 * self.sigma_pp
                    - 6 * self.m1sq * self.ESF.Q2 * (2 * self.s1hat + 3 * self.sigma_pp)
                )
            )
        ) / (
            self.deltap ** 5 * self.s1hat
        )


class F2IntrinsicSm(PartonicChannelHeavyIntrinsic):
    def fhat(self):
        return (
            32
            * self.L_xi
            * np.sqrt(self.m1sq * self.m2sq)
            * (self.deltap ** 2 - 6 * self.m1sq * self.ESF.Q2)
            * (self.m2sq + self.s1hat)
        ) / self.deltap ** 5 + (
            16
            * np.sqrt(self.m1sq * self.m2sq)
            * (
                self.deltap ** 2 * (4 * self.m2sq + 3 * self.s1hat - self.sigma_pp)
                - 6
                * self.ESF.Q2
                * (self.m2sq + self.s1hat)
                * (self.s1hat + self.sigma_pp)
            )
        ) / (
            self.deltap ** 4 * (self.m2sq + self.s1hat)
        )
