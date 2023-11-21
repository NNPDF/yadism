Miscellanea
===========

Target Mass Corrections
-----------------------

Following :cite:`Schienbein:2007gr`, :cite:`Goharipour:2020gsw` we provide three options:

- **exact**: is the full and involves integration
- **approximate**: is stemming from the exact, but the strcture functions in
  the integrand are evaluated at the bottom end
- **APFEL**: the one used in APFEL, similar to the exact but with g2 in
  the review (Schienbein et al.) set to 0

.. todo::

   complete

.. _fl-corrections:

:math:`F_L` definition
~~~~~~~~~~~~~~~~~~~~~~

Also the definition of :math:`F_L` is corrected by the presence of a proton
mass.
The explicit expression is given in :eqref:`26` of :cite:`Schienbein:2007gr`:

.. math::

   F^{\textrm{TMC}}_L (x, Q^2) = r^2 F^{\textrm{TMC}}_2 (x, Q^2) - 2 x F^{\textrm{TMC}}_1 (x, Q^2)

where the definition of :math:`r` is given in :eqref:`2` of the same paper:

.. math::

   r = \sqrt{1 + \frac{4 x^2 M^2}{Q^2}}

Isospin
-------

Isospin is used as a level-0 nuclear correction, just swapping the up and down
contribution, for the amount it is specified for the target hadron/nuclei.

In particular:

- for the **proton**: :math:`A=1, Z=1`, the up and down are kept as they are (default)
- for the **neutron**: :math:`A=1, Z=0`, the up and down components are fully
  swapped, such that the up coefficient function is matched to the down |PDF|
  and conversely
- for the **isoscalar**: :math:`A=2, Z=1` (it is the deuteron), the resulting
  coefficient functions will be mixed, i.e. the resulting :math:`c_u` will be
  half the original :math:`c_u` and half the original :math:`c_d` (same for the
  final :math:`c_d`)

The actual general expression is:

.. math::

   \begin{pmatrix} c'_u \\ c'_d \end{pmatrix} =
   \frac{1}{A}
   \begin{pmatrix} Z & A - Z \\ A - Z & Z \end{pmatrix}
   \begin{pmatrix} c_u \\ c_d \end{pmatrix}

In particular ``yadism`` does not operate at the level of |PDF|, thus all the
changes are applied to the coefficient functions.

Heavy Quark Mass scheme
-----------------------

.. todo::

   it is not yet implemented:

   - Pole masses (implemented)
   - MSbar masses (not implemented)
