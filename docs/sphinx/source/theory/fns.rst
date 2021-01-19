Flavor Number Schemes
=====================

|FNS| or Heavy Quark Matching Schemes are dealing with the ambiguity of including
massive quark contributions to physical cross sections. There is not a unique
prescription on how to do this and thus we implement several strategies.
Unfortunately there is no consistent implementation of the different scheme in the
commonly used tools and a comparison of the different outputs has to judged on a
case by case basis.

In general we can consider two different kinematic regimes that require a different
handling of the massive contributions: For :math:`Q^2 \sim m^2` the heavy quark should
be treated with the full mass dependence. For :math:`Q^2 \gg m^2` however the quark
should be considered massless, because otherwise a resummation of the occuring terms
:math:`\ln(m^2/Q^2)` would be required.

We define *Heavyness* as the split up of the *physical total structure functions*
into several subparts that represent the heavy quark contributions. Again this
is not a unique prescription and there are lots of ways to define physical
observables, e.g. tagging the outgoing state and imposing kinematics cuts.
However, we will *not*  use any of these definition as they are prone to be theoretically
unsafe, if not properly designed.
Instead we are defining new observables by considering new theories,
derived from the |SM| by just setting to 0 some of its bare couplings.

We are thus providing the observables **Flight**, **Fheavy** and **Ftotal** (for all the
unpolarized *kinds*).

FFNS
----
As the name |FFNS| suggests we are considering a fixed number of flavors :math:`n_f=n_l+1`
with :math:`n_l` light flavors and 1 (and only 1) heavy flavor with a finite mass :math:`m`.
The number of light quarks :math:`n_l` is arbitrary but fixed and can range between 3 and 5.
Except for intrinsic contributions we are *NOT* allowing the heavy (and the other non-existent)
|PDF| to contribute.

Although this is the most naive scheme, it is *NOT* consistently implement in
some of the commonly used tools. This scheme is adequate for :math:`Q^2\sim m^2`.

- **Flight** corresponds to the interaction of the purely light partons, i.e. the
  coefficient functions may only be a function of :math:`z,Q2` and eventually
  unphysical scales; in especially they may *NOT* depend on any quark mass.
  This definition is consistent with
  :cite:`vogt-f2nc,vogt-flnc,moch-f3nc,vogt-f2lcc,vogt-f3cc`, |QCDNUM|, but is not consistent
  with |APFEL|.
  
- **Ftotal** is *NOT* the sum of **Flight** and **Fheavy**, but contains additional terms
  **Fmissing** such as the Compton diagrams in :cite:`felix-thesis`.

- **Fheavy** is defined by having in the Lagrangian *only* the charges that are associated to the
  specific quark active. In |NC| this corresponds to the electric and weak charges of the quarks
  but in |CC| the situation is bit more envolved: we devide the |CKM|-matrix into several
  parts:

.. math::
   V_{CKM} =
   \begin{pmatrix}
      {\color{red}V_{ud}} & {\color{red}V_{us}} & {\color{green}V_{ub}}\\
      {\color{blue}V_{cd}} & {\color{blue}V_{cs}} & {\color{green}V_{cb}}\\
      {\color{purple}V_{td}} & {\color{purple}V_{ts}} & {\color{purple}V_{tb}}
   \end{pmatrix}

and associate the :blue:`blue` couplings to the charm structure functions, :green:`green` to bottom and
:purple:`purple` to top. For :math:`{\color{blue} F_{2,c}^{\color{black} \nu,p}}` this in effect amounts to

.. math::
   {\color{blue} F_{2,c}^{\color{black} \nu,p}} &=& 2x\Big\{C_{2,q}\otimes\Big[|{\color{blue}V_{cd}}|^2(d+\overline{c}) +
         |{\color{blue}V_{cs}}|^2 (s+\overline{c})\Big]\\
         &+& 2\left(|{\color{blue}V_{cd}}|^2+|{\color{blue}V_{cs}}|^2\right)C_{2,g}\otimes g\Big\}\\

Note that even heavier contributions are *NOT* available.

ZM-VFNS
-------
As the name |ZM-VFNS| suggests we are considering a variable number of *light* flavors :math:`n_f`
with :math:`n_f = n_f(Q^2)`. We associate an "activation" mass :math:`m` to the heavy quarks and
whenever :math:`Q^2 >= m^2` we consider this quark massless, otherwise infinitely massive.

This scheme is adequate for :math:`Q^2\gg m^2`.

- **Fheavy** is *NOT* defined, as quark masses are either 0 or :math:`\infty`
- **Ftotal** thus is equal to **Flight**
- **Flight** corresponds to the interaction of the purely light partons, i.e. the
  coefficient functions may only be a function of :math:`z,Q^2` and eventually
  unphysical scales; in especially they may *NOT* depend on any quark mass.

FONLL
-----
FONLL :cite:`forte-fonll` is a |GM-VFNS| that includes parts of |DGLAP| equations into the
matching conditions. In the original paper the prescription is only presented for the charm
contributions, but we extend it here to an arbitrary quark: in especially the ``NF_FF``
configuration variable as to point to the *heavy* quark, i.e. ``NF_FF=4`` for the charm
matching.

The prescription defines two separate regimes, below and above the *next* heavy quark mass
:math:`m_{n_f+1}`. For :math:`Q^2 > m_{n_f+1}^2` the |ZM-VFNS| is employed and this leads
to an inconsistency at this :math:`m_{n_f+1}` threshold.