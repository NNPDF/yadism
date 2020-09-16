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
        singular : number or callable
            delta (default: None)
        local : number or callable
            omx (default: None)
    """

    eps_integration_border = 1e-10
    """Set the integration domain restriction, see
    :ref:`Integration Note<integration-note>`"""

    eps_integration_abs = 1e-13
    """Set the integration target absolute error, see
    :ref:`Integration Note<integration-note>`"""

    def __init__(self, regular=None, singular=None, local=None):
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
            iter_ = iter(regular)
            self.regular = next(iter_, None)
            self.singular = next(iter_, None)
            self.local = next(iter_, None)
        except TypeError:
            self.regular = regular
            self.singular = singular
            self.local = local

    def __iter__(self):
        yield self.regular
        yield self.singular
        yield self.local

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
        # TODO: compile a proper comutational graph....
        # currently: compute the minimal nesting
        result_args = []
        if isinstance(other, DistributionVec):
            for c1, c2 in zip(self, other):
                if c1 is None:
                    result_args.append(c2)
                elif c2 is None:
                    result_args.append(c1)
                elif callable(c1):
                    if callable(c2):
                        result_args.append(lambda x, c1=c1, c2=c2: c1(x) + c2(x))
                    else:
                        result_args.append(lambda x, c1=c1, c2=c2: c1(x) + c2)
                else:
                    if callable(c2):
                        result_args.append(lambda x, c1=c1, c2=c2: c1 + c2(x))
                    else:
                        result_args.append(c1 + c2)
        elif callable(other):
            if self.regular is None:
                result_args.append(other)
            elif callable(self.regular):
                result_args.append(lambda x, c1=self.regular, c2=other: c1(x) + c2(x))
            else:
                result_args.append(lambda x, c1=self.regular, c2=other: c1 + c2(x))
            result_args.append(self.singular)
            result_args.append(self.local)
        else:
            # pretend to be a float
            other = float(other)
            if self.regular is None:
                result_args.append(other)
            elif callable(self.regular):
                result_args.append(lambda x, c1=self.regular, c2=other: c1(x) + c2)
            else:
                result_args.append(c1 + c2)
            result_args.append(self.singular)
            result_args.append(self.local)

        return DistributionVec(*result_args)

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
        # pretend that other is a float
        other = float(other)
        result_args = []

        for c1 in self:
            if c1 is None:
                result_args.append(None)
            elif callable(c1):
                result_args.append(lambda x, c1=c1, c2=other: c1(x) * c2)
            else:
                result_args.append(c1 * other)

        return DistributionVec(*result_args)

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
        # TODO: if not used in yadism move in the tests
        if isinstance(other, DistributionVec):
            for c1, c2 in zip(self, other):
                try:
                    if c1(x) != c2(x):
                        return False
                except TypeError:
                    if c1 != c2:
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
                # and also eventually restrict integration domain
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
        pdf_at_x = pdf_func(x)

        def ker(z):
            # cache again
            if self.regular is None:
                regular_at_z = 0
            elif callable(self.regular):
                regular_at_z = self.regular(z)
            else:
                regular_at_z = self.regular

            if self.singular is None:
                singular_at_z = 0
            elif callable(self.singular):
                singular_at_z = self.singular(z)
            else:
                singular_at_z = self.singular

            pdf_at_x_ov_z_div_z = pdf_func(x / z) / z
            # compute
            reg_integrand = regular_at_z * pdf_at_x_ov_z_div_z
            sing_integrand = singular_at_z * (pdf_at_x_ov_z_div_z - pdf_at_x)
            return reg_integrand + sing_integrand

        # actual convolution
        # ------------------

        # integrate the kernel
        if self.regular is None and self.singular is None:
            res, err = 0, 0
        else:
            res, err = scipy.integrate.quad(
                ker,
                z_min * (1 + self.eps_integration_border),
                z_max * (1 - self.eps_integration_border),
                epsabs=self.eps_integration_abs,
                points=breakpoints,
            )

        # sum the addends
        if self.local is None:
            local_at_x = 0
        elif callable(self.local):
            local_at_x = self.local(x)
        else:
            local_at_x = self.local

        res += pdf_at_x * local_at_x

        return res, err
