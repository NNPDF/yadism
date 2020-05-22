# -*- coding: utf-8 -*-
"""
Define :py:class:`DistributionVec` and its API, that are used to represent
distributions object in the coefficient function definition and calculation.
"""
import copy

import numpy as np
import scipy.integrate

from eko.interpolation import BasisFunction


class DistributionVec:
    r"""
        :py:class:`DistributionVec` is an object that encodes the structure of a
        distribution, as opposed to a regular function. It consists of an array of
        functions, considered as coefficients of the following distributions basis:

        - *regular*: the regular part is the coefficient of 1, so it is the pure
          function component
        - *delta*: it is the coefficient of the Dirac delta function :math:`\delta(1-x)`
        - *omx*: it is the coefficient of the distribution :math:`1/(1-x)_+`
        - *logomx*: it is the coefficient of the distribution :math:`(\log(x)/(1-x))_+`

        Note
        ----
        Unstable: it is going to change, maybe in more directions:

        - collecting all the plus distributions in a single one, so limiting the vector
          size to be 3
        - (potential) from an array of functions to an array of numbers, using a
          canonical representation (it is always possible to swap all the functional
          part in the regular)

        Parameters
        ----------
        regular : number or callable
            regular
        delta : number or callable
            delta (default: None)
        omx : number or callable
            omx (default: None)
        logomx : number or callable
            logomx (default: None)
    """

    __names = ["regular", "delta", "omx", "logomx"]
    "Set the names for available distribution kinds"

    eps_integration_border = 1e-10
    """Set the integration domain restriction, see
    :ref:`Integration Note<integration-note>`"""

    eps_integration_abs = 1e-13
    """Set the integration target absolute error, see
    :ref:`Integration Note<integration-note>`"""

    def __init__(self, regular, delta=None, omx=None, logomx=None):
        """
            A variety of argument is accepted, in order to make the constructor
            really flexible:

            - *single object per argument*: in this case each argument will
              represent a function, taken as a coefficient of the correspondent
              distribution, the following objects are available to represent the
              requested function:

              - a *callable* object, used directly as a function
              - `None`, used to silence that bit (so it represents a 0
                coefficient) (default)
              - a *number*, used as a constant coefficient (must be a number
                format for which a float representation is available)
            - *single sequence-like argument*: it's provided just for
              convenience, it is in no way different from the above, and it
              behaves like the list has been splatted (i.e. each item of the
              sequence will be assigned to an argument);
              any length in the range (0, *max*) is available, where *max* it's
              the total number of distributions available; if the length is less
              than *max* missing argument are set to `None`
        """
        try:
            # check if regular is iterable
            comp_list = [
                x for x in regular  # pylint: disable=unnecessary-comprehension
            ]
            # if a sequence provided fill the missing slots with `None`
            for _i in range(len(self.__names) - len(regular)):
                comp_list.append(None)
        except TypeError:
            # if single arguments are chosen build up a list with their values
            comp_list = [regular, delta, omx, logomx]

        # zip names with values
        components = zip(self.__names, comp_list)

        # check the type of each value and recast to a suitable callable
        for name, component in components:
            if callable(component):
                component_func = component
            elif component is None:
                component_func = lambda x: 0
            else:
                # if component is None:
                component_func = lambda x, component=component: float(component)

            setattr(self, f"_{name}", component_func)

    def __getitem__(self, key):
        """
            Implements dictionary semantics for :py:class:`DistributionVec`.

        """
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return getattr(self, f"_{name}")
        else:
            raise IndexError("todo")

    def __setitem__(self, key, value):
        """
            Implements dictionary semantics for :py:class:`DistributionVec`.

        """
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return setattr(self, f"_{name}", value)
        else:
            raise IndexError("todo")

    def __iter__(self):
        """
            Implements iterable semantics for :py:class:`DistributionVec`.

        """
        for n in self.__names:
            yield getattr(self, f"_{n}")

    def __add__(self, other):
        """
            Implements addition semantics for :py:class:`DistributionVec`.

            Supported further addends:

                - `+ num`: if a number is provided is considered as a constant
                  regular function, to be summed to the regular bit
                - `+ function`: if a callable is provided is considered as a
                  regular function to be summed to the regular bit
                - `+ DistributionVec`: if a :py:class:`DistributionVec` is
                  provided the coefficients of that one and the current one are
                  summed element-wise

            Note
            ----
            Do not support ``DistributionVec + iterable``, if needed use:

            .. code-block::

                d_vec + DistributionVec(*iterable)

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
        """
            Implements addition semantics for :py:class:`DistributionVec`, makes
            use of :py:meth:`__add__`.

        """
        return self.__add__(other)

    def __iadd__(self, other):
        """
            Implements addition semantics for :py:class:`DistributionVec`, makes
            use of :py:meth:`__add__`.

        """
        return self.__add__(other)

    def __mul__(self, other):
        """
            Implements addition semantics for :py:class:`DistributionVec`.

            The only supported type for the further factor is a scalar, and it
            is considered in a vector sense: multiplying by a scalar yields
            multiplying each coefficient by a scalar.

            Note
            ----
            Currently multiplication by a function (a callable in the code) is
            not supported, because a Distribution can only be multiplied by a
            test function (and the TestFunction API is not going to be
            implemented).

        """
        result = DistributionVec(0)
        for i, el in enumerate(self):
            result[i] = lambda x, el=el, other=other: el(x) * float(other)

        return result

    def __rmul__(self, other):
        """
            Implements addition semantics for :py:class:`DistributionVec`, makes
            use of :py:meth:`__mul__`.

        """
        return self.__mul__(other)

    def __imul__(self, other):
        """
            Implements addition semantics for :py:class:`DistributionVec`, makes
            use of :py:meth:`__mul__`.

        """
        return self.__mul__(other)

    def compare(self, other, x):
        """
            Compare two :py:class:`DistributionVec` at a given value of `x`,
            checking if all the coefficients compare equal when evaluated at
            `x`.

            Parameters
            ----------
            other :
                the other :py:class:`DistributionVec` to be compareed with the
                current one
            x :
                the kinematics point at which the comparison should be performed

            Raises
            ------
            ValueError
                The only kind of comparison available is between two
                :py:class:`DistributionVec`, so if the first argument provided
                does not match the type an error is raised.

        """
        if isinstance(other, DistributionVec):
            for c1, c2 in zip(self, other):
                if c1(x) != c2(x):
                    return False
            return True
        else:
            raise ValueError("Comparison only available with other DistributionVec")

    def convolution(self, x, pdf_func):
        r"""
            Convolute the current :py:class:`DistributionVec` with a function
            ``pdf_func``.

            The definition of the convolution performed is:

            .. math::
                \int_x^{1} \frac{\text{d}z}{z} dvec(z) f\left(\frac{x}{z}\right)

            (notice that is symmetryc in :math:`dvec \leftrightarrow f`).

            .. _integration-note:

            Note
            ----
            The class level attributes :py:attr:`eps_integration_abs` and
            :py:attr:`eps_integration_border` regulate the integration process,
            setting respectively the absolute error and restricting the
            integration domain in order to avoid singularities.

            Parameters
            ----------
            x : scalar
                the kinematics point at which the convoution is evaluated
            pdf_func : callable
                the function to be convoluted with the current
                :py:class:`DistributionVec` (usually a PDF, or a PDF
                interpolator)

            Returns
            -------
            float
                the result of the convolution
            float
                the integration error

            Note
            ----
            The real name of this method is ``convnd``.

            .. todo::
                document how the convolution is performed (that is how it's
                replaced by an integration and some pre-integrated addends)

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

        # integrate the kernel
        res, err = scipy.integrate.quad(
            ker,
            z_min * (1 + self.eps_integration_border),
            z_max * (1 - self.eps_integration_border),
            epsabs=self.eps_integration_abs,
            points=breakpoints,
        )

        # sum the addends
        for a in addends:
            res += a

        return res, err
