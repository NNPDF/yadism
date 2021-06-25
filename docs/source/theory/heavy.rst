Heavy Quark Contributions
=========================

These kind of contributions account for all those cases in which there is at
least one massive quark, but not in the input state (for these ones see
:doc:`intrinsic`).

Two masses contributions are never accounted for, so it is only considered the
case in which all massive fermion lines belong to the same flavor (lighter ones
are considered massless, while heavier are considered infinitely massive).

There is always a kinematic cut included in the case of massive corrections, due
to the need to generate the massive quark

- in the case of |NC| is applied as a cut: 

   .. math::

      Q^2 \frac{1-z}{z} > 4 m_h^2

- in the case of |CC| is applied modifying the convolution point

Asymptotic
----------

They stem from the heavy contributions, and they are the actual asymptotic limit
for very large :math:`Q^2`.

Only logarithmic terms are retained, while all the power contributions are
removed (thus the asymptotic limit can be null).

They are needed to construct the :ref:`theory/fns:FONLL` scheme.

