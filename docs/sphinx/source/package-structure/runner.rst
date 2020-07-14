Runner
======

The `Runner` class is used to provide a unique entry point to `yadism`
functionalities.

In order to compute any kind of observable a `Runner` instance should be
created, and fed with the proper theory (in the shape of a python
:class:`dict`) and the observables runcard (also as a python :class:`dict`).

.. admonition:: I/O

   Dealing with runcards as files is not a goal of `Runner`, so you can just load
   yourself whatever kind of file format you prefer (`json`, `yaml`, any type of
   db), you just need to manage the conversion step from/into a :class:`dict`.

   Almost in the same way you can/must manage the output as well (an `output
   object`__ is provided, but you can ask instead for a bare :py:class:`dict`,
   or ask the object itself for the equivalent :class:`dict`).

   __ Output_

Getting the results
-------------------
There are two ways to obtain the results from :mod:`yadism`:

- :meth:`get_result`: in this way the package will compute the coefficient
  functions, interpolating with the basis functions (it is unique once the
  ``xgrid`` and the ``polynomial_degree`` is specified) and returning the table
  of the observables at the requested points with an open index over the PDF
  vector dimension and flavour.

  It is also possible to ask the :class:`Runner` to dump directly the results
  on a file.
- :meth:`apply`: in this case a PDF object is needed, and the :class:`Runner`
  will compute the coefficient functions and apply immediately the convolution

  This method is available also as :meth:`__call__`, i.e. by calling the
  :class:`Runner` instance as a function object.

Output
~~~~~~
The original structure of the output returned by the :class:`Runner` is an
:class:`Output` object, that organizes all the elements of the computed table
in his attributes.

.. hint::

   The :class:`Output` object can be conveniently to be used, but there is no
   reason why you should.

   You can do the same by calling the :meth:`dump` method of the instance,
   saving the content on a file, reload in your favorite way and apply any
   transformation or whatever you need at a later stage.

Handlers objects
----------------
Some **handlers objects** are used to dispatch some isolated services. They are
mostly not defined internally in :mod:`yadism` package, but mainly imported from
:mod:`eko`.

Another common trait that characterize these handlers is the presence of a
method :func:`from_dict`, with which the object can be created loading the
required options directly from a suitable dictionary (that in a :class:`Runner`
object is always either `theory` or `observable` dictionary).

Interpolator Dispatcher
~~~~~~~~~~~~~~~~~~~~~~~
This object is responsible for any interpolation, so it holds the definition of
the interpolation basis, and it's able to provide them when requested.

The interpolation used is the `lagrangian
<https://en.wikipedia.org/wiki/Lagrange_polynomial>`_
one, over the ``xgrid`` provided as input.

.. admonition:: xgrid

   In principle there is no need to require that the ``xgrid`` on which the
   PDFs are interpolated should be used for all the integrations, but in
   practice a single ``xgrid`` specifications is allowed.

Constants
~~~~~~~~~
This object is only a container for the physical constants, like the *number of
colors*, and it is also locked by default, such that the default value cannot
be overwritten (if the lock is not explicitly removed).

Thresholds Config
~~~~~~~~~~~~~~~~~
Tracks the use of number of flavours all around in the code.

It is loaded with the thresholds for the heavy quark masses and the chosen
scheme, and returns the number of flavours at the given energy when asked.

Strong Coupling
~~~~~~~~~~~~~~~
This handler provide the value of the running strong coupling at the requested
energy, managing the evolution from the reference value.

There are multiple methods provided for the solution of the RGE, among which:

- *exact*: the exact numerical RK solution with the :math:`\beta` -function at
  the order specified
- *expanded*: an analytical perturbative solution, obtained by expanding the
  integrated equation consistently at the requested order

Coupling Constants
~~~~~~~~~~~~~~~~~~
In contrast this handler is defined inside the same :mod:`yadism`, and it is
responsible for managing the values related to the couplings (i.e. the
representation of each particle), but not the running couplings like
:math:`\alpha_s` or the fine structure :math:`\alpha`.
