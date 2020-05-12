# -*- coding: utf-8 -*-
"""
Define DistributionVec and its API.

.. todo::
    docs
"""
import copy

import numpy as np
import scipy.integrate

from eko.interpolation import BasisFunction


class DistributionVec:
    """
    Representing a distribution giving coefficients on a distribution basis:
        - 1
        - delta(1-x)
        - 1/(1-x)_+
        - (log(1-x)/(1-x))_+
    """

    __names = ["regular", "delta", "omx", "logomx"]
    eps_integration_border = 1e-10
    eps_integration_abs = 1e-13

    def __init__(self, regular, delta=None, omx=None, logomx=None):
        try:
            comp_list = [x for x in regular]
            for i in range(len(self.__names) - len(regular)):
                comp_list.append(None)
        except TypeError:
            comp_list = [regular, delta, omx, logomx]

        components = zip(self.__names, comp_list)

        for name, component in components:
            if callable(component):
                component_func = component
            elif component is None:
                component_func = lambda x: 0
            else:
                # if component is None:
                # __import__("pdb").set_trace()
                component_func = lambda x, component=component: float(component)

            setattr(self, f"_{name}", component_func)

    def __getitem__(self, key):
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return getattr(self, f"_{name}")
        else:
            raise IndexError("todo")

    def __setitem__(self, key, value):
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return setattr(self, f"_{name}", value)
        else:
            raise IndexError("todo")

    def __iter__(self):
        for n in self.__names:
            yield getattr(self, f"_{n}")

    def __add__(self, other):
        """
        Do not support ``DistributionVec + iterable``, if needed use:
        .. code-block::
            d_vec + DistributionVec(*iterable)

        Supported:
        * ``+ num``
        * ``+ function``
        * ``+ DistributionVec``

        .. todo::
            docs
        """
        if isinstance(other, DistributionVec):
            result = DistributionVec(0)
            for i, (c1, c2) in enumerate(zip(self, other)):
                result[i] = lambda x, c1=c1, c2=c2: c1(x) + c2(x)
        elif callable(other):
            result = copy.deepcopy(self)
            old = result[0]
            result[0] = lambda x, old=old, other=other: old(x) + other(x)
        else:
            result = copy.deepcopy(self)
            old = result[0]
            result[0] = lambda x, old=old, other=other: old(x) + float(other)

        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        """
        Supported:
        * ``+ num``

        .. note::
            Currently multiplication by a function is not supported, because a
            Distribution can only be multiplied by a test function (and the TestFunction
            API is not going to be implemented).

        .. todo::
            docs
        """
        result = DistributionVec(0)
        for i, el in enumerate(self):
            result[i] = lambda x, el=el, other=other: el(x) * float(other)

        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def compare(self, other, x):
        "Compare two DistributionVec @ x"
        if isinstance(other, DistributionVec):
            for c1, c2 in zip(self, other):
                if c1(x) != c2(x):
                    return False
            return True
        else:
            raise ValueError("Comparison only available with other DistributionVec")

    def convolution(self, x, pdf_func):
        """
            convolution.

            Parameters
            ----------
            x :
                x
            pdf_func :
                pdf_func

            .. note::
                real name of this method: ``convnd``

            .. todo::
                docs
        """
        # empty domain?
        if x >= (1 - self.eps_integration_border):
            return 0.0, 0.0
        # eko environment?
        if isinstance(pdf_func, BasisFunction):
            if pdf_func.is_below_x(x):
                # support below x --> trivially 0
                return 0.0, 0.0
            else:
                # set breakpoints as relevant points of the integrand
                # computed from interpolation areas of `pdf_func`
                # and also restrict integration domain
                area_borders = []
                for area in pdf_func.areas:
                    area_borders.extend([area.xmin, area.xmax])
                area_borders = np.unique(area_borders)
                if pdf_func._mode_log:
                    area_borders = np.exp(area_borders)
                breakpoints = x / area_borders
                z_min = x
                z_max = min(max(breakpoints), 1)
        else:  # provide default parameters
            breakpoints = []
            z_min = x
            z_max = 1

        # providing integrands functions and addends
        # ------------------------------------------

        # cache values
        self_at_1 = [e(1 - self.eps_integration_border) for e in self]
        pdf_at_x = pdf_func(x)

        def ker(z):
            # cache again
            self_at_z = [e(z) for e in self]
            pdf_at_x_ov_z_div_z = pdf_func(x / z) / z
            # compute
            res = self_at_z[0] * pdf_at_x_ov_z_div_z  # regular
            # keep delta bit in addendum (for now)
            # iterate plus distributions
            for j, (pd_at_z, pd_at_1) in enumerate(zip(self_at_z, self_at_1), -2):
                # skip
                if j < 0:
                    continue
                res += (
                    (pd_at_z * pdf_at_x_ov_z_div_z - pd_at_1 * pdf_at_x)
                    / (1.0 - z)
                    * np.log(1 - z) ** (j)
                )
            return res

        # addends
        addends = [
            0.0,
            self_at_1[1] * pdf_at_x,
            self_at_1[2] * pdf_at_x * np.log(1 - x),
            self_at_1[3] * pdf_at_x * np.log(1 - x) ** 2 / 2,
        ]

        # actual convolution
        # ------------------

        res, err = scipy.integrate.quad(
            ker,
            z_min * (1 + self.eps_integration_border),
            z_max * (1 - self.eps_integration_border),
            epsabs=self.eps_integration_abs,
            points=breakpoints,
        )
        for a in addends:
            res += a

        return res, err
