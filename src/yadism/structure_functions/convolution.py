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
        breakpoints = [x, 1.0]

        # eko environment?
        if isinstance(pdf_func, BasisFunction):
            if pdf_func.is_below_x(np.log(x)):  # TODO: in eko update remove np.log
                # support below x --> trivially 0
                return 0.0, 0.0
            else:
                # set breakpoints as relevant points of the integrand
                # computed from interpolation areas of `pdf_func`
                for area in pdf_func.areas:
                    breakpoints.extend([area.xmin, area.xmax])
                breakpoints = x / np.exp(np.unique(breakpoints))

        # providing integrands functions and addends
        # ------------------------------------------

        # plus distribution test function
        __pd_tf = lambda z, n: self[n](z) * pdf_func(x / z) / z

        integrands = [
            lambda z: self[0](z) * pdf_func(x / z) / z,
            # 0.0,
            0.0,
            lambda z: (__pd_tf(z, 2) - __pd_tf(1, 2)) / (1 - z),
            # 0.0,
            lambda z: (__pd_tf(z, 3) - __pd_tf(1, 3)) * np.log(1 - z) / (1 - z),
            # 0.0,
        ]

        addends = [
            0.0,
            self[1](1) * pdf_func(x),
            self[2](1) * pdf_func(x) * np.log(1 - x),
            self[3](1) * pdf_func(x) * np.log(1 - x) ** 2 / 2,
        ]

        # actual convolution
        # ------------------

        res = 0.0
        err = 0.0

        for i, a in zip(integrands, addends):
            if callable(i):
                r, e = scipy.integrate.quad(
                    i,
                    x * (1 + self.eps_integration_border),
                    1.0 * (1 - self.eps_integration_border),
                    points=breakpoints,
                )

                res += r
                err += e
            res += a

        return res, err
