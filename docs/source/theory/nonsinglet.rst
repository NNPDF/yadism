Non-singlet definition
======================

From Vogt 3-loop paper :eqref:`4.1` :cite:`vogt-f2nc`, we get:

.. math::

   x^{-1} F = C_{ns} \otimes q_{ns} + \ev{e^2} \left(C_q \otimes q_s + C_g \otimes g\right)

where:

.. math::

   C_q = C_{ns} + C_s


Basis definition
----------------

The "singlet" is the actual *flavor singlet*:

.. math::

   q_s = \sum_q  (q + \bar{q})


The so called "non-singlet" is actually the difference between the *charged
singlet* and the *flavor singlet*:

.. math::

   q_{ns} = \sum_q \left(e_q^2 - \ev{e^2}\right) ~ (q + \bar{q})


Of course they are both *singlet-like* (referring to evolution basis) since
they are proportional to :math:`q_+`

.. math::

   q_+ = q + \bar{q}


This basis is natural because NC cannot distinguish a flavor from the
anti-flavor (instead CC can).

Charged Current
~~~~~~~~~~~~~~~

CC can be treated in an analogous way, simply:

- when the incoming quark is *directly* coupling (*non-singlet*) to the EW boson
  (so :math:`W_{\pm}`) only the flavor or the anti-flavor may have a non-zero
  coupling, but not both
- when the incoming quark is *indirectly* coupling through a gluon (*singlet*)
  nothing change, because the average has to be done on half the objects, but
  being an average this amounts to multiply and divide by :math:`2`

Equivalent expression (`yadism`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An equivalent expression is:

.. math::

   C_{ns} \otimes \left(\sum\nolimits_q e_q^2 ~ q_+\right) +
   C_{ps} \otimes \left(\sum\nolimits_q \ev{e^2} ~ q_+\right)\\

so in `yadism` we are using:

- the name **non-singlet** to call the *charged singlet*:

  - in which every quark is weighted with the square of its charge

- the name **singlet** to call the *flavor singlet*:

  - in which every quark is weighted with the average of all the square charges
    of the quark that are taking part

Indeed:

.. math::

   C_{ns} \otimes q_{ns} &+ \ev{e^2} (C_{ns} + C_{ps}) \otimes q_s\\
   C_{ns} \otimes \left( \sum\nolimits_q (e_q^2 - \ev{e^2}) ~ q_+ \right) &+
   \ev{e^2} (C_{ns} + C_{ps}) \otimes \left( \sum\nolimits_q q_+\right) \\
   \sum\nolimits_q q_+ \otimes ( C_{ns}  (e_q^2 - \ev{e^2}) &+ \ev{e^2} (C_{ns} + C_{ps}) ) )\\
   \sum\nolimits_q q_+ \otimes ( C_{ns}  e_q^2 &+ \ev{e^2} C_{ps} ) )

Inducing from LO structure functions
------------------------------------

To retrieve the exact definition of :math:`q_{ns}` in :cite:`vogt-f2nc` we assumed:

- :math:`q_s = \sum\nolimits_q q_+(x)`, i.e. the *singlet* is the *flavor singlet*
- and we compare the LO DIS expressions

.. math::

   x^{-1} F_2(x) &=  \sum\nolimits_q e_q^2 ~ q_+(x) \\
   x^{-1} F_2(x) &=  q_{ns}(x) + \ev{e^2} q_s(x)\\
   &=  q_{ns}(x) + \ev{e^2} \sum\nolimits_q q_+(x) 

Where:

- the first equation is the |LO| |DIS| result in the flavor basis
- the second one is the way it is expressed in :cite:`vogt-f2nc`

Consider the following hypothesis on the number of flavors:

- :math:`n_f=1`:

.. math::

   x^{-1} F_2(x) &= e_u^2 ~ u_+(x) \stackrel{!}{=} q_{ns}(x) + e_u^2 u_+(x)\\
   &\Rightarrow q_{ns}(x) = e_u^2 u_+(x) - e_u^2 u_+(x) = 0

- :math:`n_f=2`:

.. math::


   x^{-1} F_2(x)  &= e_u^2 u_+(x) + e_d^2 d_+(x) \stackrel{!}{=} q_{ns}(x) +
   \frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) )\\
   &\Rightarrow q_{ns}(x) = e_u^2 u_+(x) + e_d^2 d_+(x) - \frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) ) 

Then:

.. math::

   q_{ns}(x) = \sum_q (e_q^2 - \ev{e^2}) ~ q_+(x)
