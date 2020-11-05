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

:py:class:`EvaluatedStructureFunctionLight` :
    this class is inheriting from the former, factorizing some common procedure
    needed for light calculation.

:py:class:`EvaluatedStructureFunctionHeavy` :
    this class is inheriting from the former, factorizing some common procedure
    needed for heavy quark calculation, like matching schemes
"""

import copy
import logging

import numpy as np

from . import distribution_vec as conv
from .esf_result import ESFResult

logger = logging.getLogger(__name__)


class EvaluatedStructureFunction:
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

        .. admonition:: Cache

            A part of the overall caching system is implemented at this level.

            The one implemented here is only a **local, isolated** caching,
            i.e.:

            - the first time the instance is asked for computing the result,
              through the :py:meth:`get_output` method, it registers the result;
            - any following call to the :py:meth:`get_output` method will make
              use of the cached result, and will never recompute it.

            If another instance with the same attributes is asked for the result
            it will recompute it from scratch, because any instance is isolated
            and doesn't keep any reference to the others.

        Parameters
        ----------
            SF : StructureFunction
                the parent :py:class:`StructureFunction` instance, provides an
                interface, holds references to global objects (like managers coming
                from :py:mod:`eko`, e.g. :py:class:`InterpolatorDispatcher`) and
                implements the global caching
            kinematics : dict
                the specific kinematic point as a dict with two elements ('x', 'Q2')

    """

    def __init__(self, SF, kinematics: dict):
        x = kinematics["x"]
        if 1 < x <= 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1]")
        if kinematics["Q2"] <= 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")
        # check domain
        if x < min(SF.interpolator.xgrid_raw):
            raise ValueError(f"x outside xgrid - cannot convolute starting from x={x}")

        self._SF = SF
        self._x = x
        self._Q2 = kinematics["Q2"]
        self._res = ESFResult(x=self._x, Q2=self._Q2)
        self._computed = False

        if not self._SF.obs_name.is_composed:
            self.partonic_channels = self._SF.partonic_channels
            self.weights = self._SF.weights
            self.convolution_point = self._SF.convolution_point(
                self._x, self._Q2, self._SF.M2hq
            )

        logger.debug("Init %s", self)

    def __repr__(self):
        return "%s(x=%f,Q2=%f)" % (self._SF.obs_name, self._x, self._Q2)

    def _compute_local(self):
        """
            Here is where the local caching is actually implemented: if the
            coefficient functions are already computed don't do nothing,
            otherwise call :py:meth:`_compute_component` (checks are per flavour).

            In any case no output is provided, but the result is stored in
            instance's attributes (this method is for internal use).
        """
        # something to do?
        if self._computed:
            return
        # run
        logger.debug("Compute %s", self)
        for comp_cls in self.partonic_channels:
            comp = comp_cls(self)
            (
                self._res.values[comp.label],
                self._res.errors[comp.label],
            ) = self._compute_component(comp)
        # add the factor x from the LHS
        self._res *= self.convolution_point
        # setup weights
        self._res.weights = self.weights(
            self._SF.obs_name, self._SF.coupling_constants, self._Q2
        )

    def _compute_component(self, comp):
        """
            Perform coefficient function calculation for a single flavour,
            combining orders, compute the convolution through
            :py:meth:`DistributionVec.convolution` iterating over *basis
            functions* and take care of scale variations.

            Parameters
            ----------
            f_LO : callable, or sequence of callables
                implements LO coefficient function
            f_NLO : callable, or sequence of callables
                implements NLO coefficient function
            f_NLO_fact : callable, or sequence of callables
                implements NLO factorization scheme contribution

            .. todo::
                reference needed for factorization scheme
        """
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(comp["LO"]())
        if self._SF.pto > 0:
            a_s = self._SF.strong_coupling.a_s(self._Q2 * self._SF.xiR ** 2)
            d_vec += a_s * (
                conv.DistributionVec(comp["NLO"]())
                + (-np.log(self._SF.xiF ** 2))
                * conv.DistributionVec(comp["NLO_fact"]())
            )

        # iterate all polynomials
        for polynomial_f in self._SF.interpolator:
            cv, ecv = d_vec.convolution(self.convolution_point, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return np.array(ls), np.array(els)

    def get_result(self):
        """
            Compute actual result

            Returns
            -------
            res : ESFResult
                result
        """
        self._compute_local()

        return copy.deepcopy(self._res)

    def get_output(self) -> dict:
        """
            Returns the output for this instance.

            In particular it returns the convolution of the coefficient function
            for the selected observable and the array of basis functions, so the
            result will be an array itself, running over the interpolation grid.

            Caching is provided as explained in the class description (see
            :py:class:`EvaluatedStructureFunction`).

            Returns
            -------
            dict
                a collection of the output arrays with the following structure:

                - `x`: the input momentum fraction
                - `Q2`: the input process scale
                - `values`: a :py:meth:`numpy.array` for the coefficient functions
                - `errors`: a :py:meth:`numpy.array` with the integration errors

        """
        return self.get_result().get_raw()


class EvaluatedStructureFunctionLight(EvaluatedStructureFunction):
    """
        Parent class for the light ESF implementations -
        really meaning up, down, and strange quark contributions.
    """

    def __init__(self, SF, kinematics, nf=3):  # 3 = u+d+s
        super().__init__(SF, kinematics)
        # expose number of flavours
        self.nf = nf


class EvaluatedStructureFunctionHeavy(EvaluatedStructureFunction):
    """
        Specialize EvaluatedStructureFunction for heavy flavours.

        This class factorizes some common tasks needed for heavy flavours
        (namely: charm, bottom and top quarks), in particular:

        - apply heavy quark matching scheme

        .. todo::
            - document prefactor: FH page 61 (6.1), 65 (7.2) - Vogt page 21 (4.1)
            - a_s expansion factor already included (simplify with alpha_s/4pi)
                pay attention to Vogt 1/x in (4.1) in FH appendix are written
                the expressions for c's (6.1), convolution defined in (7.2)
                also the charge average 9 / 2 is coming from Vogt (4.1)
                definition in the gluon
            - remember that is only for the gluon and quark singlet, so it
                should be removed from the non-singlet prefactor
            - why is it not the pdf but xpdf used? check why Laenen is using
                xpdf in the first place
            - docs
    """

    def __init__(self, SF, kinematics, force_local=False):
        super().__init__(SF, kinematics)
        self._force_local = force_local

    def get_result(self):
        """
            .. todo::
                docs
        """
        nhq = self._SF.obs_name.hqnumber
        # get our local active number of flavors
        scheme = self._SF.threshold.scheme
        nf = self._SF.threshold.get_areas(self._Q2 * self._SF.xiF ** 2)[-1].nf
        # use local only? i.e. by force or because we (Q2) are below our threshold (name)
        if self._force_local or nf < nhq:
            # skip for ZM-VFNS -> return 0
            if scheme != "ZM-VFNS":
                self._compute_local()
        else:
            logger.debug("Apply '%s' to %s", scheme, self)
            # compute zero-mass part
            obs_name = self._SF.obs_name
            # TODO maybe we can cache the heavy light any how - for the moment we can't because of
            # the explicit n_f dependece **inside** the coefficient functions (and not only in the
            # weight)
            res_light = self._SF.get_esf(
                obs_name.apply_flavor(obs_name.flavor + "light"),
                {"x": self._x, "Q2": self._Q2},
                1,
            ).get_result()
            # now checkout scheme:
            # matching is only needed for FONLL and in there only if we just crossed our threshold
            # otherwise we continue with the ZM expressions (in contrast to APFEL which treats only
            # F2c in this way)
            # FONLL-A corresponds to (strict) APFEL
            # FONLL-A' reduces to the ZM-VFNS scheme if above the next threshold (which would
            # numerically happen anyway, but only at very large Q2)
            if (scheme == "FONLL-A" and nf >= nhq) or (
                scheme == "FONLL-A'" and nf == nhq
            ):
                # collect all parts
                res_heavy = self._SF.get_esf(
                    obs_name, {"x": self._x, "Q2": self._Q2}, force_local=True
                ).get_result()
                res_asy = self._SF.get_esf(
                    obs_name.apply_asy(), {"x": self._x, "Q2": self._Q2}
                ).get_result()
                # add damping
                damp = 1
                if self._SF.FONLL_damping:
                    power = self._SF.damping_powers[nhq - 3]
                    damp = np.power(1.0 - self._SF.M2hq / self._Q2, power)
                # join all
                self._res = res_heavy.suffix(f"_{scheme}_heavy") + damp * (
                    res_light.suffix(f"_{scheme}_light")
                    - res_asy.suffix(f"_{scheme}_asymptotic")
                )
            else:
                self._res = res_light

        return copy.deepcopy(self._res)
