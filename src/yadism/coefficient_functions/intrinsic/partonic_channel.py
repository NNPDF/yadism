# -*- coding: utf-8 -*-
import numpy as np
from eko import constants

from ..fonll import partonic_channel as pc
from ..partonic_channel import RSL, PartonicChannel
from . import raw_nc


class NeutralCurrentBase(pc.PartonicChannelAsyIntrinsic):
    def __init__(self, *args, m1sq, m2sq):
        super().__init__(*args, m1sq=m1sq, m2sq=m2sq)
        self.sigma_pp = self.Q2 + self.m2sq + self.m1sq
        self.sigma_mp = self.Q2 - self.m2sq + self.m1sq

    def init_nlo_vars(self):
        self.I1 = raw_nc.I1(self)
        self.Cplus = raw_nc.Cplus(self)
        self.C1m = raw_nc.C1m(self)
        self.C1p = raw_nc.C1p(self)
        self.CRm = raw_nc.CRm(self)
        self.S = raw_nc.S(self)
        self.L_xisoft = np.log(
            (self.sigma_pp - self.delta) / (self.sigma_pp + self.delta)
        )

    def init_vars(self, z):
        self.s1hat = (
            (1.0 - z)
            * ((self.delta - self.sigma_pm) * z + self.delta + self.sigma_pm)
            / 2.0
            / z
        )
        self.deltap = self.kinematic_delta(self.m1sq, self.s1hat + self.m2sq, -self.Q2)
        self.L_xi = np.log(
            (self.sigma_pp + self.s1hat - self.deltap)
            / (self.sigma_pp + self.s1hat + self.deltap)
        )

    def mkNLO(self, kind, RS):
        self.init_nlo_vars()
        norm = 2.0 * constants.CF * self.eta / self.x  # 2 = as_norm
        omx = norm * raw_nc.__getattribute__(  # pylint: disable=no-member
            f"f{kind}_{RS}_soft"
        )(self)

        delta = norm * (
            raw_nc.__getattribute__(f"f{kind}_{RS}_virt")(  # pylint: disable=no-member
                self
            )
            + self.S  # add normalization between curly and upright F
            * raw_nc.__getattribute__(f"m{kind}_{RS}")(  # pylint: disable=no-member
                self
            )
        )

        def reg(z, _args):
            self.init_vars(z)
            return norm * raw_nc.__getattribute__(  # pylint: disable=no-member
                f"f{kind}_{RS}_raw"
            )(self) - omx / (1.0 - z)

        return RSL.from_distr_coeffs(reg, (delta, omx))


class ChargedCurrentBase(PartonicChannel):
    """
    The convolution point simplifies to :math:`x` when m2=0,
    see :eqref:`6` of :cite:`kretzer-schienbein`.
    """

    def __init__(self, *args, m1sq):
        super().__init__(*args)
        self.m1sq = m1sq
        self.y = -self.ESF.Q2 / m1sq
