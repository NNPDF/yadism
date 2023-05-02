from .. import partonic_channel as epc
from ..partonic_channel import RSL
from . import nlo, nnlo
from . import partonic_channel as pc


# For gL, the LO contribution vanishes
class NonSinglet(pc.LightBase):
    @staticmethod
    def NLO():
        """
        |ref| implements NLO-part of :eqref:`A.1`, :cite:`Zijlstra-light-nnlo-pol`.
        """

        return RSL(nlo.fl.ns_reg)

    def NNLO(self):
        """
        |ref| implements :eqref:`19`, :cite:`Borsa-light-nnlo-pol`.
        """

        return RSL(
            nnlo.xclns2p.clnn2a, loc=nnlo.xclns2p.clnn2c, args=dict(reg=[self.nf])
        )


class Gluon(epc.EmptyPartonicChannel):
    pass


class Singlet(epc.EmptyPartonicChannel):
    pass
