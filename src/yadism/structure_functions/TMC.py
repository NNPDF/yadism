# -*- coding: utf-8 -*-
"""
Runner: holds a list of structure functions instances, that will act as our
"soft singletons"
StructureFunction: holds a reference to his parent runner, in this way its also
able to access its StructureFunctions siblings (like F2 from FL, in order to
compute TMCs, e.g.)

Caching: it is managed at the level of StructureFunction, while the values are
kept at the level of ESF (so the StructureFunction is just routing the caller to
the correct instance of ESF to ask for values)

Note 1
------
Here is the third time that we are proliferating the SF classes to all the
flavours and kinds (SF/ESFTMC/ESF x 2/L x light/c/b/t), but at the bottom level
they are needed (ESF implementation are actually different for every option, so
it makes sense to have different classes).
The classes one level above (SF/ESFTMC) are simply shadowing the ones below in
order to route to the correct one. The same business can be done with a `switch`
pattern (actually `if...elif...elif...` in python), but the only difference is
how many lines of code you are saving.
**Proposal** for a better layout in which we don't need to explicitly shadow
from level to level (and we don't need to route with `if` as well) are liked and
likeòy to be accepted.

Note 2 (caching)
----------------
Since the responsibility of caching is of SF as written above we decided the
following layout:
    - SF instantiate ESF or ESFTMC according to TMC flag in theory dictionary,
      and append it to `self.__ESFs` at load time, i.e. in `self.load()` (these
      are the observables to be computed)
    - when asked for output if noTMC a ESF is called and the instance is
      registered
        - `self.get_ouput()` is used for getting the result passing through:
        - `self.get_ESF()` is used for getting the instance and register to the
          cache
    - if TMC a ESFTMC is called, and whenever he needs an ESF instance to
      compute a point it will ask its parent SF with `SF.get_ESF()` method, in
      this way passing through the cache

Note 3 (physics)
----------------
There 3 schemes in the reference:
    - **exact**: is the full and involves integration
    - **approximate**: is stemming from the exact, but the strcture functions in
      the integrand are evaluated at the bottom end
    - **APFEL**: the one used in APFEL, similar to the exact but with one of the
      integral of the review (schienbein, functions h_2 and f_2) set to 0, Felix
      knows which

.. todo::
    docs
"""
import abc
import warnings

import numpy as np
from scipy.integrate import quad

from .convolution import DistributionVec


class EvaluatedStructureFunctionTMC(abc.ABC):
    """
        .. todo:
            docs
    """

    def __init__(self, SF, kinematics):
        self._SF = SF
        self._flavour = SF._name[2:]
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]

        self._mu = self._SF._M2target / self._Q2
        self._rho = np.sqrt(1 + 4 * self._x ** 2 * self._mu)
        self._xi = 2 * self._x / (1 + self._rho)

        self._shifted_kinematics = {"x": self._xi, "Q2": self._Q2}

        self._out = kinematics

    @abc.abstractmethod
    def _get_output_APFEL(self):
        """
            .. todo:
                docs
        """

    @abc.abstractmethod
    def _get_output_approx(self):
        """
            .. todo:
                docs
        """

    @abc.abstractmethod
    def _get_output_exact(self):
        """
            .. todo:
                docs
        """

    def get_output(self):
        """
            .. todo:
                docs
        """
        if self._SF._TMC == 0:  # no TMC
            raise RuntimeError(
                "EvaluatedStructureFunctionTMC shouldn't have been created as TMC is disabled."
            )
        if self._SF._TMC == 1:  # APFEL
            return self._get_output_APFEL()
        if self._SF._TMC == 2:  # approx
            return self._get_output_approx()
        if self._SF._TMC == 3:  # exact
            return self._get_output_exact()
        if self._SF._TMC == 4:  # approx_APFEL
            warnings.warn("meant only for internal use")
            raise NotImplementedError("approx. APFEL not implemented yet")
        raise ValueError(f"Unkown TMC value {self._SF._TMC}")

    def _integrate_F2(self,ker):
        # compute F2 matrix (j,k) (where k is wrapped inside get_output)
        F2list = []
        skip = 0
        for xj in self._SF._interpolator.xgrid_raw:
            # in domain
            #if xj <= self._xi:
            #    skip += 1
            #    continue
            # collect support points
            F2list.append(self._SF.get_ESF(
                "F2" + self._flavour, {"Q2": self._Q2, "x": xj}
            ).get_output())
        # compute interpolated h2 integral (j)
        h2list = []
        j = 0
        for bf in self._SF._interpolator:
            #if j < skip:
            #    j += 1
            #    continue
            d = DistributionVec(ker)
            h2list.append(d.convolution(self._xi,bf))
        # init result (k)
        res = {}
        for f in ["q", "g", "q_error", "g_error"]:
            res[f] = np.zeros(len(self._SF._interpolator.xgrid_raw))
        # multiply along j
        j = 0
        for h2, f2elem in zip(h2list,F2list):
            #if j < skip:
            #    j += 1
            #    continue
            for f in ["q", "g"]:
                res[f] += h2[0] * f2elem[f]
                res[f+"_error"] += np.abs(h2[1]* f2elem[f]) + np.abs(h2[0]* f2elem[f+"_error"])
        return res

    def _h2(self):
        """
            Compute integral over F2.


        """
        return self._integrate_F2(lambda z,xi=self._xi: 1/xi * z)


class ESFTMC_F2(EvaluatedStructureFunctionTMC):
    def _get_output_approx(self):
        # fmt: off
        approx_prefactor = (
            self._x ** 2 / (self._xi ** 2 * self._rho ** 3)
            * (1 + (6 * self._mu * self._x * self._xi)
                    / self._rho * (1 - self._xi) ** 2)
        )
        # fmt: on

        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_output()

        for f in ["q", "g", "q_error", "g_error"]:
            self._out[f] = approx_prefactor * F2out[f]

        return self._out

    def _get_output_APFEL(self):
        factor_shifted = self._x ** 2 / (self._xi ** 2 * self._rho ** 3)
        factor_h2 = 6.0 * self._x ** 3 * self._mu / (self._rho ** 4)

        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_output()

        h2out = self._h2()
        for f in ["q", "g", "q_error", "g_error"]:
            self._out[f] = factor_shifted * F2out[f] + factor_h2 * h2out[f]
        return self._out

    def _get_output_exact(self):
        raise NotImplementedError("TODO")


class ESFTMC_FL(EvaluatedStructureFunctionTMC):
    def _get_output_approx(self):
        approx_prefactor_FL = self._x ** 2 / (self._xi ** 2 * self._rho)

        # fmt: off
        approx_prefactor_F2 = approx_prefactor_FL * (
            (4 * self._mu * self._x * self._xi) / self._rho * (1 - self._xi)
            + 8 * (self._mu * self._x * self._xi / self._rho) ** 2
                * (-np.log(self._xi) - 1 + self._xi)
        )
        # fmt: on

        FLout = self._SF.get_ESF(
            "FL" + self._flavour, self._shifted_kinematics
        ).get_output()
        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_output()

        for f in ["q", "g", "q_error", "g_error"]:
            self._out[f] = (
                approx_prefactor_FL * FLout[f] + approx_prefactor_F2 * F2out[f]
            )

        return self._out

    def _get_output_APFEL(self):
        raise NotImplementedError("TODO")

    def _get_output_exact(self):
        raise NotImplementedError("TODO")


ESFTMCmap = {"F2": ESFTMC_F2, "FL": ESFTMC_FL}
