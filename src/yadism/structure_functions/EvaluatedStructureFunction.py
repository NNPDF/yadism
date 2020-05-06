# -*- coding: utf-8 -*-
"""
This module provides the base classes that define the interface for Structure
Function calculation on a given kinematic point (x, Q2) (that is why they are
called *Evaluated*).
They are:

:py:class:`EvaluatedStructureFunction` :
    this is a pure abstract class, that define the interface (defining the way
    in which coefficient functions are actually encoded) and implement some
    shared methods (like initializer and :py:meth:`get_output`, responsible also
    for :ref:`local caching<local-caching>`.

:py:class:`EvaluatedStructureFunctionHeavy` :
    this class is inheriting from the former, factorizing some common procedure
    needed for heavy quark calculation, like auxiliary variable definition,
    threshold passing calculation or directly setting to 0 some coefficient
    functions.
"""
import abc

import numpy as np

from . import convolution as conv


class EvaluatedStructureFunction(abc.ABC):
    """
        The actual Structure Function implementation.

        This class is the abstract class that implements the structure for all
        the coefficient functions' providers, for a single kinematic point (x,
        Q2), but all the flavours (singlet, nonsinglet, gluon).

        Since the coefficient functions in general are distributions they are
        provided with an internal representation, that respects the interface
        defined by the class :py:class:`conv.DistributionVec`, and the same
        class is used to perform the convolution with the basis functions (see
        :py:class:`eko.InterpolatorDispatcher`), so the final result will
        consist of an array of dimension 2: one dimension corresponding to the
        interpolation grid, the other to the flavour.

        Its subclasses are organized by:

        - kind: `F2`, `FL`
        - flavour: `light`, `charm`, `bottom`, `top`

        and they all implement a :py:meth:`get_output` method that performs the
        calculation (convolution included), if needed.

        .. _local-caching:

        Caching
        ~~~~~~~

        A part of the overall caching system is implemented at this level.

        The one implemented here is only a **local, isolated** caching, i.e.:

        - the first time the instance is asked for computing the result, through
          the :py:meth:`get_ouput` method, it registers the result;
        - any following call to the :py:meth:`get_output` method will make use
          of the cached result, and will never recompute it.

        If another instance with the same attributes is asked for the result it
        will recompute it from scratch, because any instance is isolated and
        doesn't keep any reference to the others.

        Parameters
        ----------
        SF : StructureFunction
            the parent :py:class:`StructureFunction` instance, provides an
            interface, holds references to global objects (like managers coming
            from :py:mod:`eko`, e.g. :py:class:``) and implements the global caching
        kinematics : dict
            the specific kinematic point as a dict with two elements ('x', 'Q2')

        Methods
        -------
        get_output()
            compute the coefficient functions
    """

    def __init__(self, SF, kinematics: dict):
        """
            Internal Attributes
            -------------------

            _SF :
                parent :py:class:`StructureFunction` reference
            _x :
                momentum fraction
            _Q2 :
                process energy
            _cqv :
                singlet quark coefficient function (implements the cache)
            _e_cqv :
                error on :py:attr:`_cqv`
            _cgv :
                gluon coefficient function (implements the cache)
            _e_cgv :
                error on :py:attr:`_cgv`
            _a_s :
                value of $ \alpha_s / 4 \pi $ at the scale :py:attr:`_Q2`
            _n_f :
                number of flavours at the scale :py:attr:`_Q2`
        """
        if 1 < kinematics["x"] < 0:

            raise ValueError("Kinematics 'x' must be in the range (0,1)")
        if kinematics["Q2"] < 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")

        self._SF = SF
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        self._cqv = []
        self._e_cqv = []
        self._cgv = []
        self._e_cgv = []
        self._a_s = self._SF._alpha_s.a_s(self._Q2 * self._SF._xiR ** 2)
        self._n_f = self._SF._threshold.get_areas(self._Q2)[-1].nf

    def _compute(self):
        """
            Here is where the local caching is actually implemented: if the
            coefficient functions are already computed don't do nothing,
            otherwise call :py:meth:`_compute_component` (checks are per flavour).

            In any case no output is provided, but the result is stored in
            instance's attributes (this method is for internal use).
        """
        # something to do?
        if not self._cqv:
            # yes
            self._cqv, self._e_cqv = self._compute_component(
                self.quark_0, self.quark_1, self.quark_1_fact
            )
        if not self._cgv:
            # yes
            self._cgv, self._e_cgv = self._compute_component(
                self.gluon_0, self.gluon_1, self.gluon_1_fact
            )

    def _compute_component(self, f_LO, f_NLO, f_NLO_fact):
        """
            Perform coefficient function calculation for a single flavour,
            combining orders, compute the convolution through
            :py:meth:`DistributionVec.convolution` iterating over *basis
            functions* and take care of scale variations.

            Parameters
            ----------
            f_LO : :py:class:`conv.DistributionVec`
                implements LO coefficient function
            f_NLO : :py:class:`conv.DistributionVec`
                implements NLO coefficient function
            f_NLO_fact : :py:class:`conv.DistributionVec`
                implements NLO factorization scheme contribution

            .. todo::
                reference needed for factorization scheme
        """
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(f_LO())
        if self._SF._pto > 0:
            d_vec += self._a_s * (
                conv.DistributionVec(f_NLO())
                + 2  # TODO: to be understood
                * (-np.log(self._SF._xiF ** 2))
                * conv.DistributionVec(f_NLO_fact())
            )

        # iterate all polynomials
        for polynomial_f in self._SF._interpolator:
            cv, ecv = d_vec.convolution(self._x, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return ls, els

    def get_output(self):
        """
        .. todo::
            docs
        """
        self._compute()

        output = {}
        output["x"] = self._x
        output["Q2"] = self._Q2
        output["q"] = self._cqv
        output["q_error"] = self._e_cqv
        output["g"] = self._cgv
        output["g_error"] = self._e_cgv
        return output

    @abc.abstractmethod
    def quark_0(self):
        """
            quark coefficient function at order 0 in :math`a_s`
        """
        pass

    def gluon_0(self):
        """
            gluon coefficient function at order 0 in :math`a_s`

            Set to 0 for all kind of observables and flavours, since there is no
            gluon contribution at order 0.
        """
        return 0

    @abc.abstractmethod
    def quark_1(self):
        """
            quark coefficient function at order 1 in :math`a_s`
        """
        pass

    @abc.abstractmethod
    def quark_1_fact(self):
        """
            quark factorization scheme contribution, at order 1 in :math`a_s`

            .. todo::
                - docs
                - consistent naming convention: use hep-ph/0006154 convention
                  of c_a^(l,m), e.g. quark_1_fact -> quark_1_1
                  also take care of muR, since in reference eq.2.16 they are
                  setting muR = muF, so maybe quark_1_fact -> quark_1_1_0
        """
        pass

    @abc.abstractmethod
    def gluon_1(self):
        """
            gluon coefficient function at order 1 in :math`a_s`
        """
        pass

    @abc.abstractmethod
    def gluon_1_fact(self):
        """
            gluon factorization scheme contribution, at order 1 in :math`a_s`

            .. todo::
                docs
        """
        pass


class EvaluatedStructureFunctionHeavy(EvaluatedStructureFunction):
    def __init__(self, SF, kinematics, charge_em):
        super(EvaluatedStructureFunctionHeavy, self).__init__(SF, kinematics)

        # FH - Vogt comparison prefactor
        # TODO: document prefactor
        # FH page 61 (6.1), 65 (7.2) - Vogt page 21 (4.1)
        # a_s expansion factor already included (simplify with alpha_s / 4 pi)
        # pay attention to Vogt 1/x in (4.1)
        # in FH appendix are written the expressions for c's (6.1), convolution
        # defined in (7.2)
        # also the charge average 9 / 2 is coming from Vogt (4.1) definition in the
        # gluon
        # TODO: remember that is only for the gluon and quark singlet, so it should
        # be removed from the non-singlet prefactor
        # TODO: why is it not the pdf but xpdf used? check why Laenen is using xpdf
        # in the first place
        self._charge_em = charge_em
        self._FHprefactor = self._Q2 / (np.pi * self._SF._M2) * 9 / 2  # / self._x

        # common variables
        self._s = self._Q2 * (1 - self._x) / self._x
        self._shat = lambda z: self._Q2 * (1 - z) / z

        self._rho_q = -4 * self._SF._M2 / self._Q2
        self._rho = lambda z: -self._rho_q * z / (1 - z)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

    def is_below_threshold(self, z):
        """
        .. todo::
            use threshold on shat or using FH's zmax?
        """
        return self._shat(z) <= 4 * self._SF._M2

    def quark_0(self) -> float:
        return 0

    def quark_1(self):
        return 0

    def quark_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0

    @abc.abstractmethod
    def _gluon_1(self):
        pass

    def gluon_1(self):
        if self._s <= 4 * self._SF._M2:
            return 0
        else:
            return self._gluon_1()

    def gluon_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0
