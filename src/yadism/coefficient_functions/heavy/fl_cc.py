import numpy as np

from .. import splitting_functions as split
from ..partonic_channel import RSL
from . import partonic_channel as pc


class NonSinglet(pc.ChargedCurrentNonSinglet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sf_prefactor = 1.0 - self.labda

    def NLO(self):
        """
        |ref| implements :eqref:`A.1-4` with Table 1, :cite:`gluck-ccheavy`.
        """
        a = self.ka
        b1 = lambda z: (
            2.0 - 2.0 * z**2 - 2.0 / z - self.labda * (1.0 - 4.0 * z + z**2)
        )
        b2 = lambda z: 2.0 / z - 1.0 - z - self.labda * (z - z**2)

        return self.h_q(a, b1, b2)


class Gluon(pc.ChargedCurrentGluon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sf_prefactor = 1.0 - self.labda

    def NLO(self):
        """
        |ref| implements :eqref:`A.5-7` with Table 2, :cite:`gluck-ccheavy`.
        """
        as_norm = 2.0

        def reg(z, _args):
            c1 = 8.0 * self.labda**2 - 6.0 * self.labda + 2.0
            c2 = 0.0
            c3 = 4.0 * self.labda
            c4 = -8.0 * self.labda
            return (
                (
                    self.sf_prefactor
                    * (split.lo.pqg_single(z, np.array([], dtype=float)) / 2.0)
                    * (self.l_labda(z) - np.log(self.labda))
                )
                + self.h_g(z, [c1, c2, c3, c4])
            ) * as_norm

        return RSL(reg)
