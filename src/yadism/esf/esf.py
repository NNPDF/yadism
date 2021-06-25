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

from .. import coefficient_functions as cf
from . import conv
from . import scale_variations as sv
from .result import ESFResult

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
        self.orders = list(filter(lambda e: e <= SF.pto, range(2 + 1)))

        logger.debug("Init %s", self)

    def __repr__(self):
        return "%s_%s(x=%f,Q2=%f)" % (self.sf.obs_name, self.process, self.x, self.Q2)

    @property
    def zeros(self):
        return np.zeros((len(br.flavor_basis_pids), len(self.sf.interpolator.xgrid)))

    def compute_local(self):
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
        full_orders = [(o, 0, 0, 0) for o in self.orders]
        # prepare scale variations
        sv_manager = self.sf.sv_manager
        if sv_manager is not None:
            full_orders = sv.build_orders(self.sf.pto)
        # init orders with 0
        for o in full_orders:
            self.res.orders[o] = [self.zeros, self.zeros]
        # run
        logger.debug("Compute %s", self)
        # iterate all partonic channels
        for cfe in cfc.collect_elems():
            ker_orders = {}
            # compute raw coefficient functions
            for o in self.orders:
                rsl = cfe.coeff[o]()
                if rsl is None:
                    continue
                # compute convolution point
                convolution_point = cfe.coeff.convolution_point()
                val, err = conv.convolute_vector(
                    rsl, self.sf.interpolator, convolution_point
                )
                # add the factor x from the LHS
                val, err = convolution_point * val, convolution_point * err
                partons = np.array(
                    [cfe.partons.get(pid, 0.0) for pid in br.flavor_basis_pids]
                )[:, np.newaxis]
                val = val[np.newaxis, :]
                err = err[np.newaxis, :]
                ker_orders[(o, 0, 0, 0)] = (partons, val, err)

            # apply scale variations
            if sv_manager is not None:
                ker_orders.update(
                    sv_manager.apply_common_scale_variations(ker_orders, cfc.nf)
                )
                ker_orders.update(
                    sv_manager.apply_diff_scale_variations(ker_orders, cfc.nf)
                )

            # blow up to flavor space
            for o, (partons, val, err) in ker_orders.items():
                self.res.orders[o][0] += partons @ val
                self.res.orders[o][1] += np.abs(partons) @ err

        self._computed = True

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
