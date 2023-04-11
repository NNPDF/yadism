# -*- coding: utf-8 -*-
import LeProHQ
import numpy as np
from scipy.integrate import quad

from ..partonic_channel import RSL
from . import partonic_channel as pc

class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.3`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("x2g1", "VV", self._xi, self._eta(z))
            )
        return RSL(cg)
    
    def NNLO(self):
        """
        |ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`.

        The equation is composed of the coefficient function (here denoted by cg1) :eqref:`D.14` and the scaling coefficient function (here denoted by cgBar1) :eqref:`D.35`.

        The different parts of the coefficient function are as follows:

        The part proportional to ln^2(beta), :eqref:`D.15`.
        The part proportional to ln(beta), :eqref:`D.16`.
        The finite 'OK' (non-abelian) part, :eqref:`D.20`.
        The finite 'QED' (abelian) part, :eqref:`D.26`.

        This equation is the same as the F3 and F2 of the unpolarized case.
        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("x2g1", "VV", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("x2g1", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )
        return RSL(cg)
    

class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.6`, :cite:`felix-thesis`. 

        This is the same result as GluonVV at NLO.

        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("x2g1", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """
        |ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`.

        The equation is composed of the coefficient function (here denoted by cg1) :eqref:`D.14` and the scaling coefficient function (here denoted by cgBar1) :eqref:`D.38`.

        The different parts of the coefficient function are as follows:

        The part proportional to ln^2(beta), :eqref:`D.15`.
        The part proportional to ln(beta), :eqref:`D.16`.
        The finite 'OK' (non-abelian) part, :eqref:`D.23`.
        The finite 'QED' (abelian) part, :eqref:`D.29`.

        This equation is the same as the F3 of the unpolarized case.
        
        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("x2g1", "AA", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("x2g1", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class SingletVV(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`.
        
        The NLO Bethe-Heitler Quark coefficient function :eqref:`D.43` is made up of the following parts: 

        The part proportional to ln(beta) :eqref:`D.44`.
        The constant part is defined in :eqref:`D.48`.

        The NLO Bethe-Heitler quark scaling coefficient functions :eqref:`D.51` is denoted by cqBarF1.

        """

        def cq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("x2g1", "VV", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("x2g1", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class SingletAA(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`.

        The NLO Bethe-Heitler Quark coefficient function (here denoted by cq1) :eqref:`D.43` is made up of the following parts: 

        The part proportional to ln(beta) :eqref:`D.44`.
        The constant part is defined in :eqref:`D.46`.

        The NLO Bethe-Heitler quark scaling coefficient function :eqref:`D.54` is denoted by cqBarF1.
        """

        def cq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("x2g1", "AA", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("x2g1", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)
    

class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) non-singlet coefficient function, :cite:`felix-thesis`.

        This function should be the same in the VV and AA case, and should correspond to the zF3 VA of the unpolarized coefficient function.

        Implements :eqref:`D.64`.
        """

        def dq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (LeProHQ.dq1("x2g1", "VV", self._xi, self._eta(z)))
            )

        return RSL(dq)

    
#todo: write out numerical results for the gluon VV and gluon AA using the results of felix's thesis and then assert equality 


#Personal Tests Below --> attribute x is for some reason not part of ESF

#sf = StructureFunction(observable_name.ObservableName("F2_light"),Runner(theory_params, observable_name.ObservableName("FL_light")),)

# kinematics = []
# kinematics.extend([dict(x=0.1, Q2=20.0, y=0)])

# theory = copy.deepcopy(theories.default_card)
# observable = copy.deepcopy(observables.default_card)
# observable["observables"]["F2_light"] = kinematics


# run_instance = Runner(theory, observable,)
# managers = run_instance.get_managers() 

# sf =  compute_sf()
# kinematics = dict(x=0.1, Q2=20.0)
# esf = ESF(kinematics, sf, configs= managers )
# pc_instance = PartonicChannel(ESF = esf)
# nc_instance = pc.NeutralCurrentBase(pc_instance, m2hq= 10,)
# gvv_instance = GluonVV(nc_instance)
# result = gvv_instance.NLO()