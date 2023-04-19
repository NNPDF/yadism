import numpy as np

from .. import splitting_functions as split
from ..partonic_channel import RSL
from . import partonic_channel as pc


class NonSinglet(pc.ChargedCurrentNonSinglet):
    def NLO(self):
        """
        |ref| implements :eqref:`A.1-4` with Table 1, :cite:`gluck-ccheavy`.
        """
        a = self.ka
        b1 = lambda z: 2 - 2 * z**2 - 2 / z
        b2 = lambda z: 2 / z - 1 - z

        return self.h_q(a, b1, b2)


class Gluon(pc.ChargedCurrentGluon):
    def NLO(self):
        """
        |ref| implements :eqref:`A.5-7` with Table 2, :cite:`gluck-ccheavy`.
        """
        as_norm = 2.0

        def reg(z, _args):
            c1 = (
                12.0 * (1 - self.labda) ** 2 - 18 * (1 - self.labda) + 8
            )  # =12l^2 - 6l +2
            c2 = (1.0 - self.labda) / (1.0 - self.labda * z) - 1.0
            c3 = 6.0 * self.labda
            c4 = -12.0 * self.labda
            return (
                (
                    split.lo.pqg_single(z, np.array([], dtype=float))
                    / 2.0
                    * (self.l_labda(z) - np.log(self.labda))
                )
                + self.h_g(z, [c1, c2, c3, c4])
            ) * as_norm

        return RSL(reg)
