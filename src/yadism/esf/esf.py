# -*- coding: utf-8 -*-
"""
This module provides the base class that define the interface for Structure
Function calculation on a given kinematic point (x, Q2) (that is why they are
called *Evaluated*).
"""

import copy
import logging

import numpy as np

from eko import basis_rotation as br

from . import conv
from .result import ESFResult
from .. import coefficient_functions as cf

logger = logging.getLogger(__name__)


class EvaluatedStructureFunction:
    """
    A specific kinematic point for a specific structure function.

    This class implements the structure for all
    the coefficient functions' providers, for a single kinematic point (x,
    Q2), but all the flavours (singlet, nonsinglet, gluon).

    Since the coefficient functions in general are distributions they are
    provided with an internal representation, that respects the interface
    defined by the class :py:class:`conv.DistributionVec`, and the same
    class is used to perform the convolution with the basis functions (see
    :py:class:`eko.InterpolatorDispatcher`), so the final result will
    consist of an array of dimension 2: one dimension corresponding to the
    interpolation grid, the other to the flavour.

    .. _local-caching:

    .. admonition:: Cache

        A part of the overall caching system is implemented at this level.

        The one implemented here is only a **local, isolated** caching,
        i.e.:

        - the first time the instance is asked for computing the result,
          through the :py:meth:`get_result` method, it registers the result;
        - any following call to the :py:meth:`get_result` method will make
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
        if x > 1 or x <= 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1]")
        if kinematics["Q2"] <= 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")
        # check domain
        if x < min(SF.interpolator.xgrid_raw):
            raise ValueError(f"x outside xgrid - cannot convolute starting from x={x}")

        self.sf = SF
        self.x = x
        self.Q2 = kinematics["Q2"]
        self.nf = None
        self.process = SF.runner.managers["coupling_constants"].obs_config["process"]
        self.res = ESFResult(self.x, self.Q2, None)
        self._computed = False
        # select available partonic coefficient functions
        self.orders = filter(lambda e: e <= SF.pto, range(2 + 1))

        logger.debug("Init %s", self)

    def __repr__(self):
        return "%s_%s(x=%f,Q2=%f)" % (self.sf.obs_name, self.process, self.x, self.Q2)

    @property
    def zeros(self):
        return np.zeros((len(br.flavor_basis_pids), len(self.sf.interpolator.xgrid)))

    def compute_local(self, sv=None):
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
        cfc = cf.Combiner(self)
        # run
        logger.debug("Compute %s", self)
        # init order with 0
        for o in self.orders:
            self.res.orders[(o, 0, 0, 0)] = (self.zeros, self.zeros)
            # iterate all partonic channels
            for cfe in cfc.collect_elems():
                rsl = cfe.coeff[o]()
                if rsl is None:
                    continue
                # compute convolution point
                convolution_point = cfe.coeff.convolution_point()
                val, err = self.compute_coefficient_function(convolution_point, rsl)
                # blow up to flavor space
                for pid, w in cfe.partons.items():
                    pos = br.flavor_basis_pids.index(pid)
                    self.res.orders[(o, 0, 0, 0)][0][pos] += w * val
                    self.res.orders[(o, 0, 0, 0)][1][pos] += np.abs(w) * err

        # prepare convolutions
        if sv is not None:
            self.include_scale_variations(sv, cfc.nf)

        self._computed = True

    def include_scale_variations(self, sv, nf):
        for alphas_power in self.orders:
            for lnf_power in range(alphas_power):
                self.res.orders[(alphas_power, 0, 0, lnf_power)] = (
                    self.zeros,
                    self.zeros,
                )
                for lnrf_power in range(alphas_power - 1):
                    self.res.orders[(alphas_power, 0, lnrf_power, lnf_power)] = (
                        self.zeros,
                        self.zeros,
                    )
        # apply factorization scale variations matrices
        for ((alphas_power, lnf_power), src), mat in sv.fact_matrices(nf):
            v, e = self.res.orders[(src, 0, 0, 0)]
            self.res.orders[(alphas_power, 0, 0, lnf_power)][0] += mat @ v
            self.res.orders[(alphas_power, 0, 0, lnf_power)][1] += mat @ e

        # apply ren/fact scale variations
        for (
            (alphas_power, lnrf_power),
            src,
        ), coeff in sv.fact_to_ren_prefactors(nf):
            for lnf_power in range(alphas_power):
                v, e = self.res.orders[(src, 0, 0, lnf_power)]
                self.res.orders[(alphas_power, 0, lnrf_power, lnf_power)][0] = coeff * v
                self.res.orders[(alphas_power, 0, lnrf_power, lnf_power)][1] = coeff * e

    def compute_coefficient_function(self, convolution_point, cf):
        """
        Perform coefficient function calculation for a single stack of
        coefficient functions,
        combining orders, compute the convolution through
        :meth:`DistributionVec.convolution` iterating over *basis
        functions* and take care of scale variations.

        Parameters
        ----------
        comp : yadism.partonic_channel.PartonicChannel
            Coefficient function to be computed

        Returns
        -------
            ls : list(float)
                values
            els : list(float)
                errors
        """

        ls = []
        els = []
        # iterate all polynomials
        for polynomial_f in self.sf.interpolator:
            c, e = conv.convolution(cf, convolution_point, polynomial_f)
            # add the factor x from the LHS
            c, e = c * convolution_point, e * convolution_point
            ls.append(c)
            els.append(e)
        return np.array(ls), np.array(els)

    def get_result(self):
        """
        Compute actual result

        Returns
        -------
        res : ESFResult
            result
        """
        self.compute_local()

        return copy.deepcopy(self.res)
