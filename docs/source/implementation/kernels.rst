Kernels
=======

The coefficient functions consist of the partonic cross-sections, that have to
be convolved with the PDFs in order to obtain the hadronic structure functions,
according to the factorization theorem:

.. math::

   F(x) = \sum_i f_i \otimes c_i (x) = \int_x^1 \frac{dz}{z}
   f_i\left(\frac{x}{z}\right) c_i(z)

So actually there is a coefficient function for each PDF (i.e. for each flavor).

The actual physical combination are not as many as flavors, indeed |QCD| is
flavor blind (in the massless case, and the only difference in the massive case
are the value of the masses themselves).

In particular there are 3 relevant combinations, for polarized and
unpolarized |DIS| as described in :doc:`../theory/coeff-funcs`.

.. todo::

   - describe kernel structure
   - stress that there are four kinds:

     - in *non-singlet* channel allows to reuse a single integration for multiple
       channels, that there the line directly connects to the EW boson
     - in *gluon* and *singlet* the incoming line is always decoupled by a
       *gluon* from the EW and thus naturally appears the charge average (that
       depend on the number of flavors running in the loops)
     - that *intrinsic* is treated separately (heavy-initiated)

   - stress that Charged Current are slightly different from Neutral ones, and
     point to the corresponding theory section
   - describe that kernels are defined as (partons, coefficient) and turned into
     (partons, operator, operator-error) by convolutions


Singlet & Non-singlet
---------------------

For the distinction about singlet and non-singlet coefficient function,
see :doc:`../theory/nonsinglet`.
