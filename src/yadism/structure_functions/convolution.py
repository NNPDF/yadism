# -*- coding: utf-8 -*-
"""
Define DistributionVec and its API.

.. todo::
    docs
"""
import numpy as np
import scipy.integrate


class DistributionVec:
    """
    Representing a distribution giving coefficients on a distribution basis:
        - 1
        - delta(1-x)
        - 1/(1-x)_+
        - (log(1-x)/(1-x))_+
    """

    __names = ["regular", "delta", "omx", "logomx"]

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
                f = float(component)
                component_func = lambda x: f

            setattr(self, f"_{name}", component_func)

    def __getitem__(self, key):
        if key == 0:
            return self._regular
        elif key == 1:
            return self._delta
        elif key == 2:
            return self._omx
        elif key == 3:
            return self._logomx
        else:
            raise ValueError("todo")

    def __iter__(self):
        return NotImplemented

    def convnd(self, x, pdf_func):
        """TODO: Docstring for convnd.

        Parameters
        ----------
        self : TODO
        x : TODO
        pdf : TODO

        Returns
        -------
        TODO

        """

        # providing integrands functions and addends
        # ------------------------------------------

        # plus distribution test function
        __pd_tf = lambda z, n: self[n](z) * pdf_func(x / z) / z

        integrands = [
            lambda z: self[0](z) * pdf_func(x / z) / z,
            0.0,
            lambda z: (__pd_tf(z, 2) - __pd_tf(1, 2)) / (1 - z),
            lambda z: (__pd_tf(z, 3) - __pd_tf(1, 3)) * np.log(1 - z) / (1 - z),
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
                    i, x, 1.0, points=[x, 1.0]
                )  # TODO: take care of both limits
                res += r
                err += e ** 2
            res += a

        return res, np.sqrt(err)
