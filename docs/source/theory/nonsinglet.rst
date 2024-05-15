Non-singlet definition
======================

From Vogt 3-loop paper :eqref:`4.1` :cite:`vogt-f2nc`, we get:

.. math::

   x^{-1} F = C_{ns} \otimes q_{ns}^{+} + \ev{e^2} \left(C_q \otimes q_s + C_g \otimes g\right)

where:

.. math::

   C_q = C_{ns} + C_s


Photon Exchange
---------------

In the syntax of :cite:`vogt-f2nc` "singlet" is the actual *flavor singlet*:

.. math::

   q_s = \sum_q  (q + \bar{q})


The so called "non-singlet" is actually the difference between the *charged
singlet* and the *flavor singlet*:

.. math::

   q_{ns}^{+} = \sum_q \left(e_q^2 - \ev{e^2}\right) ~ (q + \bar{q})


Of course they are both *singlet-like* (referring to evolution basis) since
they are proportional to :math:`q_+`

.. math::

   q_+ = q + \bar{q}


This basis is natural because EM cannot distinguish a flavor from the
anti-flavor (instead NC or CC can).


Equivalent expression (`yadism`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An equivalent expression is:

.. math::

   x^{-1} F = C_{ns} \otimes \left(\sum_q e_q^2 ~ q_+\right) + C_{ps} \otimes \left(\sum_q \ev{e^2} ~ q_+\right)\\

so in `yadism` we are using:

- the name **non-singlet** to call the *charged singlet*:

  - in which every quark is weighted with the square of its charge

- the name **singlet** to call the *flavor singlet*:

  - in which every quark is weighted with the average of all the square charges
    of the quark that are taking part

Indeed:

.. math::

   x^{-1} F(x) &= C_{ns} \otimes q_{ns}^{+} + \ev{e^2} (C_{ns} + C_{ps}) \otimes q_s\\
   &= C_{ns} \otimes \left( \sum_q (e_q^2 - \ev{e^2}) ~ q_+ \right) + \ev{e^2} (C_{ns} + C_{ps}) \otimes \left( \sum_q q_+\right) \\
   &= \sum_q q_+ \otimes ( C_{ns}  (e_q^2 - \ev{e^2}) + \ev{e^2} (C_{ns} + C_{ps}) ) )\\
   &= \sum_q q_+ \otimes ( C_{ns}  e_q^2 + \ev{e^2} C_{ps} ) )

Inducing from LO structure functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve the exact definition of :math:`q_{ns}^{+}` in :cite:`vogt-f2nc` we assumed:

- :math:`q_s = \sum\nolimits_q q_+(x)`, i.e. the *singlet* is the *flavor singlet*
- and we compare the LO DIS expressions

.. math::

   x^{-1} F_2(x) &=  \sum_q e_q^2 ~ q_+(x) \\
   &=  q_{ns}^{+}(x) + \ev{e^2} q_s(x)\\
   &=  q_{ns}^{+}(x) + \ev{e^2} \sum_q q_+(x)

Where:

- the first equation is the |LO| |DIS| result in the flavor basis
- the second one is the way it is expressed in :cite:`vogt-f2nc`

Consider the following hypothesis on the number of flavors:

- :math:`n_f=1`:

.. math::

   x^{-1} F_2(x) &= e_u^2 ~ u_+(x) \stackrel{!}{=} q_{ns}^{+}(x) + e_u^2 u_+(x)\\
   &\Rightarrow q_{ns}^{+}(x) = e_u^2 u_+(x) - e_u^2 u_+(x) = 0

- :math:`n_f=2`:

.. math::


   x^{-1} F_2(x)  &= e_u^2 u_+(x) + e_d^2 d_+(x) \stackrel{!}{=} q_{ns}^{+}(x) +
   \frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) )\\
   &\Rightarrow q_{ns}^{+}(x) = e_u^2 u_+(x) + e_d^2 d_+(x) - \frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) )

Then:

.. math::

   q_{ns}^{+}(x) = \sum_q (e_q^2 - \ev{e^2}) ~ q_+(x)


Neutral Current
---------------

The case of parity conserving |NC| structure functions is analogous to |EM|,
just with different coupling and summing all the electroweak channels.
However, for parity violating structure functions (e.g. :math:`F_3`)
we have a different decompositions:

.. math::

   x^{-1} F_3 = C_{ns} \otimes q_{ns}^{-} + \ev{e^2} \left(C_q \otimes q_v\right)

where the two quark flavor combinations are defined as

.. math::

   q_v & = \sum_q  (q - \bar{q}) \\
   q_{ns}^{-} &= \sum_q \left(g_q^2 - \ev{g^2}\right) ~ (q - \bar{q})

and :math:`g_q` is a suitable electroweak coupling.
As before in yadism we rotate the coefficients to a new basis.

.. math::

   x^{-1} F_3 = C_{ns} \otimes \left(\sum\nolimits_q e_q^2 ~ q_-\right) +
   C_{v} \otimes \left(\sum\nolimits_q \ev{e^2} ~ q_-\right)

with

.. math::

   q_- = q - \bar{q}

Note that neither the gluon nor the flavor singlet can generate a parity violating term.

Charged Current
---------------

|CC| can be treated in an analogous way:

- when the incoming quark is *directly* coupling (*non-singlet*) to the |EW| boson
  (i.e. :math:`W^{\pm}`) only the flavor or the anti-flavor may have a non-zero
  coupling, but not both
- when the incoming quark is *indirectly* coupling through a gluon (*singlet*)
  nothing change, because the average has to be done on half the objects, but
  being an average this amounts to multiply and divide by :math:`2`


Higher Orders
-------------

The decomposition of the quark sector in different partonic channels
has the advantage to facilitate the relations with higher orders
|QCD| corrections.

- :math:`C_{ns}` is always the leading contribution as it corresponds
  to diagrams in which the incoming flavor is coupling directly to the
  electroweak boson.
- :math:`C_{g}` is suppressed by :math:`\mathcal{O}(a_s)`
  as the gluon need to radiate a quark-antiquark pair before coupling
  with a electroweak boson.
- :math:`C_{ps},C_{v}` are suppressed by :math:`\mathcal{O}(a_s^2)` or
  :math:`\mathcal{O}(a_s^3)` respectively as they are related to diagrams
  where the incoming flavor line is not coupling directly with the electroweak boson.

From |N3LO| on a new class of diagrams, called :math:`fl_{11}`, can appear for
the parity conserving structure functions, both in the quark and gluon sector
:cite:`Larin:1996wd`. In these diagrams the incoming and outgoing bosons are
coupling to different fermion lines (open or in loops) and thus generate
contributions that  are not proportional to the coupling squared :math:`g_q^2`,
or its average :math:`\ev{g^2}`, but rather to :math:`\ev{g} g_q` for quarks or
:math:`\ev{g}^2` for gluons respectively.
