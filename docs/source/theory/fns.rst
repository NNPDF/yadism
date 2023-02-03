Flavor Number Schemes
=====================

|FNS| or Heavy Quark Matching Schemes are dealing with the ambiguity of
including massive quark contributions to physical cross sections. There is not
a unique prescription on how to do this and thus we implement several
strategies. Unfortunately there is no consistent implementation of the
different schemes in the commonly used tools and a comparison of the different
outputs has to judged on a case by case basis.

In general we can consider two different kinematic regimes that require a
different handling of the massive contributions: For :math:`Q^2 \lesssim m^2`
the heavy quark should be treated with the full mass dependence. For :math:`Q^2
\gg m^2` however the quark should be considered massless, because otherwise a
resummation of the occurring terms :math:`\ln(m^2/Q^2)` would be required.

We define *Heavyness* as the split up of the *physical total structure
functions* into several subparts that represent the heavy quark contributions.
Again this is not a unique prescription and there are lots of ways to define
physical observables, e.g. tagging the outgoing state and imposing kinematics
cuts. However, we will **not**  use any of these definitions as they are prone
to be theoretically unsafe, if not properly designed.
Instead we are defining new observables by considering new theories,
derived from the |SM| by just setting to :math:`0` some of its bare couplings.

We are thus providing the observables **Flight**, **Fheavy** and **Ftotal** (for all the
unpolarized :ref:`kinds<kinds def>`).

FFNS
----
As the name |FFNS| suggests we are considering a fixed number of flavors
:math:`n_f=n_l+1` with :math:`n_l` light flavors and **1 (and only 1) heavy
flavor** with a finite mass :math:`m`. The number of light quarks :math:`n_l` is
arbitrary but fixed and can range between 3 and 5. Except for intrinsic
contributions we are *NOT* allowing the heavy (and the other non-existent)
|PDF| to contribute.

Although this is the most naïve scheme, it is *NOT* consistently implement in
some of the commonly used tools. This scheme is adequate for :math:`Q^2\sim
m^2`.

- **Flight** corresponds to the interaction of the purely light partons, i.e.
  the coefficient functions may only be a function of :math:`z,Q^2` and
  eventually unphysical scales; in especially they may *NOT* depend on any
  quark mass.
  This may be consistently obtained computing contributions for a Lagrangian
  with all masses set to :math:`0`.

  - This definition is consistent with
    :cite:`vogt-f2nc,vogt-flnc,moch-f3nc,vogt-f2lcc,vogt-f3cc`, |QCDNUM|
  - but is not consistent with |APFEL|, which instead it's calling **Flight**
    the sum of contributions in which a light quark is coupled to the |EW|
    boson (but this definition would contain massive corrections, but not
    consistently, and so it's theoretically unsafe)

- **Ftotal** is *NOT* the sum of **Flight** and the single **Fheavy**, but
  contains additional terms **Fmissing** such as the Compton diagrams in
  :cite:`felix-thesis`.
  This is the proper physical object, accounting for all contributions coming
  from the full Lagrangian.

- **Fheavy** is defined by having in the Lagrangian *only* the |EW| charges
  that are associated to the specific quark active (the only massive one). In
  |NC| this corresponds to the electric and weak charges of the quarks but in
  |CC| the situation is bit more involved: we divide the |CKM|-matrix into
  several parts:

  .. math::
     V_{CKM} =
     \begin{pmatrix}
        {\color{red}V_{ud}} & {\color{red}V_{us}} & {\color{green}V_{ub}}\\
        {\color{blue}V_{cd}} & {\color{blue}V_{cs}} & {\color{green}V_{cb}}\\
        {\color{purple}V_{td}} & {\color{purple}V_{ts}} & {\color{purple}V_{tb}}
     \end{pmatrix}

  and associate the :blue:`blue` couplings to the charm structure functions,
  :green:`green` to bottom and :purple:`purple` to top. For
  :math:`{\color{blue} F_{2,c}^{\color{black} \nu,p}}` this in effect amounts
  to

  .. math::
     {\color{blue} F_{2,c}^{\color{black} \nu,p}} &=&
     2x\Big\{C_{2,q}\otimes\Big[|{\color{blue}V_{cd}}|^2(d+\overline{c}) +
           |{\color{blue}V_{cs}}|^2 (s+\overline{c})\Big]\\
           &+&
           2\left(|{\color{blue}V_{cd}}|^2+|{\color{blue}V_{cs}}|^2\right)C_{2,g}\otimes
           g\Big\}\\

  Note that even heavier contributions are *NOT* available.
  E.g.:

  - there is no contributions coming from either *bottom* or *top* to
    :math:`F_{2,c}`
  - while *charm* would contribute to :math:`F_{2,b}`, but only as a massless
    flavor.

ZM-VFNS
-------
As the name |ZM-VFNS| suggests we are considering a variable number of *light*
flavors :math:`n_f` with :math:`n_f = n_f(Q^2)`. We associate an *activation*
scale :math:`Q_{thr, i}^2` to each *"heavy"* quark and whenever :math:`Q^2 \ge
Q_{thr, i}^2` we consider this quark massless, otherwise infinitely massive.

.. note::

   :math:`Q_{thr,i}^2` are not necessarily, but are usually chosen, to be the
   quarks' masses.

This scheme is adequate for :math:`Q^2\gg m^2`.

- **Fheavy** is *NOT* defined, as quark masses are either :math:`0` or
  :math:`\infty` (so no massive correction is available at all)
- **Ftotal** thus is equal to **Flight**
- **Flight** corresponds to the interaction of the purely light partons, i.e. the
  coefficient functions may only be a function of :math:`z,Q^2` and eventually
  unphysical scales; in especially they may *NOT* depend on any quark mass.

|ZM-VFNS| dependence on thresholds is simple, they just define the :math:`Q^2`
patches in which :math:`n_f` is constant (and they are of course different from
the quark masses, that are always considered to be zero or infinite).

FONLL
-----
| FONLL :cite:`forte-fonll` is a |GM-VFNS| that includes parts of the |DGLAP| equations into the
  matching conditions.
| That is: two different schemes are considered, and they are matched at a given
  scale, accounting for the resummation of collinear logarithms.

In the original paper the prescription is only presented for the charm
contributions, but we extend it here to an arbitrary quark.

The prescription defines two separate regimes, below and above the *next* heavy
quark threshold: :math:`Q_{thr,n_f+2}`.

.. note::

   As in the case of |ZM-VFNS|, the thresholds are not necessarily, but usually
   chosen, to be the quarks' masses.

- for :math:`Q^2 < Q_{thr,n_f+2}^2`:

   The general expression, :eqref:`14-15` of :cite:`forte-fonll`, is:

   .. math::

      F^{\textrm{FONLL}}(x, Q^2) = F^{(d)}(x, Q^2) + F^{(n_f)}(x, Q^2)\\
      F^{(d)}(x, Q^2) = F^{(n_f + 1)}(x, Q^2) - F^{(n_f, 0)}(x, Q^2)

   Here we include explicitly the scheme change between the schemes with
   :math:`n_f` (i.e. the |FFNS| scheme in which the active flavor is the only
   one considered to be massive) and :math:`(n_f + 1)` flavors (i.e. the |FFNS|
   scheme with only massless quarks, including the formerly active one).

   This scheme change is related to the |DGLAP| matching conditions: in
   particular the massive corrections are only coming from the :math:`n_f`
   scheme, but the collinear contribution is present in both:

   - the :math:`n_f` scheme includes the logarithms of the active mass,
      while the |PDF| of the massive object are scale-independent by definition
      (since the factorization terms are kept in the matrix element)
   - the :math:`(n_f + 1)` scheme does not account for them in them in the coefficient
      function, but instead they are resummed in the |PDF| evolution through the
      |DGLAP| equation

   By matching the two schemes a |GM-VFNS| is obtained, accounting for both the
   massive corrections and the resummation of collinear logarithms.

   The matching is obtained subtracting the asymptotic massless limit of the
   massive expression, namely :math:`F^{(n_f, 0)}(x, Q^2)`, while adding the
   :math:`(n_f + 1)` expression, such that for large :math:`Q^2` the massive
   :math:`n_f` contribution cancels with the asymptotic one, and only the truly
   light contribution survives.

   Actually below the former threshold, so :math:`Q^2 < Q_{thr,n_f+1}^2`, |FNS|
   with :math:`n_f` flavors is employed, i.e. a :math:`\theta(Q^2 -
   Q_{thr,n_f+1}^2)` is prepended to :math:`F^{(d)}`.


- above this threshold:

  The |ZM-VFNS| is employed and this leads to an inconsistency at this
  :math:`Q_{thr,n_f+2}` threshold, but a good approximation nevertheless.

  This amounts to simply make an hard cut to the original smooth decay of
  massive contributions, and to add the subsequent thresholds for the following
  massive quarks.

Damping
~~~~~~~

.. admonition:: Continuity

   Up to |NLO| the scheme change (from :math:`n_f - 1` flavors to :math:`n_f`) is
   continuous, but in general it is not.

   In order to recover the continuous transition a damping procedure may be
   adopted, turning the scheme in the so called **damp FONLL**.

Continuity on its own is not an issue, but it is one symptom of a feature of
:math:`F^{(d)}`: while it improves the behavior at large :math:`Q^2` it is
unreliable for :math:`Q^2 \sim Q_{thr,n_f+1}^2`.

For this reason might be a good idea to suppress :math:`F^{(d)}` near threshold,
and then this restore continuity.

The generic shape of this suppression is written in :eqref:`17` of
:cite:`forte-fonll`, and it is:

.. math::

   F^{(d, th)} (x, Q^2) = f_{\textrm{thr}} (x, Q^2) F^{(d)}(x, Q^2)

In particular the following conditions are needed for :math:`f_{\textrm{thr}}
(x, Q^2)` to fit the task:

- be such that :math:`F^{(d, th)} (x, Q^2)` and :math:`F^{(d)} (x, Q^2)` is
  power suppressed for large :math:`Q^2`
- enforce the vanishing of :math:`F^{(d, th)} (x, Q^2)` at and below threshold

A common shape for :math:`f_{\textrm{thr}} (x, Q^2)` is then:

.. math::

   f_{\textrm{thr}} (x, Q^2) = \theta(Q^2 - m^2) \left(1 -  \frac{Q^2}{m^2}\right)^2

.. note::

   The power used here is :math:`2`, but in general this is arbitrary, and thus
   it is a user choice in ``yadism``.

Threshold different from heavy quark mass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The matching scale :math:`\mu^2` seems to play a relevant role in |FONLL|, since it is deciding where (in
:math:`Q^2`) the conversion between the schemes should happen.
A typical choice is to put the matching scale on top of the relevant quark mass (also
in |ZM-VFNS|, mimicking the opening of a new channel). This is **not
mandatory**, as the matching scale is just an |FNS| parameter it can be freely
chosen.

However, in practice, choosing the matching scale *different* from the quark masses
has no effect in |FONLL| since the matching conditions follow the same
evolution as |PDF| which are inlined in either case. We demonstrate this explicitly in the following.
We follow the notation of :cite:`forte-fonll` and denote the coefficient functions
in the massive scheme (with :math:`n_f` light and 1 heavy flavor) by :math:`C^{(n_f)}`
and the coefficient functions in the mass-less scheme (with :math:`(n_f+1)` light flavors)
by :math:`B`. For the sake of readability we suppress in the following any dependence
on parton momenta (i.e. :math:`x` or :math:`z`).

.. math::

   F^{(n_f)}(Q^2) &= B \otimes f^{(n_f+1)}(Q^2)\\
      &= C^{(n_f)}(Q^2) \otimes f^{(n_f)}(Q^2) \\
      &= C^{(n_f)}(Q^2) \otimes E^{(n_f)}(Q^2 \leftarrow \mu^2) \otimes f^{(n_f)}(\mu^2) \\
      &= C^{(n_f)}(Q^2) \otimes E^{(n_f)}(Q^2 \leftarrow \mu^2) \otimes K^{-1}(\mu^2/m^2) \otimes f^{(n_f+1)}(\mu^2) \\
      &= C^{(n_f)}(Q^2) \otimes E^{(n_f)}(Q^2 \leftarrow \mu^2) \otimes K^{-1}(\mu^2/m^2) \otimes E^{(n_f+1)}(\mu^2 \leftarrow Q^2) \otimes f^{(n_f+1)}(Q^2) \\
   \Rightarrow B &= C^{(n_f)}(Q^2) \otimes E^{(n_f)}(Q^2 \leftarrow \mu^2) \otimes K^{-1}(\mu^2/m^2) \otimes E^{(n_f+1)}(\mu^2 \leftarrow Q^2)

We used the (raw) |EKO| :math:`E` for DGLAP evolution

.. math::

   f^{(n_f)}(Q^2) = E^{(n_f)}(Q^2 \leftarrow \mu^2) f^{(n_f)}(\mu^2)

and the matching conditions :math:`K` to match |PDF| between different number of light flavors

.. math::

   f^{(n_f+1)}(\mu^2) = K(\mu^2/m^2) \otimes f^{(n_f)}(\mu^2)

where we can assume that the matching scale :math:`\mu^2` might be different from the quark mass :math:`m^2`.
This latter equation we can, however, relate back to the case of :math:`\mu^2=m^2` using |EKO| again:

.. math::
   f^{(n_f+1)}(\mu^2) &= E^{(n_f+1)}(\mu^2 \leftarrow m^2) \otimes f^{(n_f+1)}(m^2)\\
      &= E^{(n_f+1)}(\mu^2 \leftarrow m^2) \otimes K(1) \otimes f^{(n_f)}(m^2)\\
      &= E^{(n_f+1)}(\mu^2 \leftarrow m^2) \otimes K(1) \otimes E^{(n_f)}(m^2 \leftarrow \mu^2) \otimes f^{(n_f)}(\mu^2)\\
   \Rightarrow K(\mu^2/m^2) &= E^{(n_f+1)}(\mu^2 \leftarrow m^2) \otimes K(1) \otimes E^{(n_f)}(m^2 \leftarrow \mu^2)

Inserting this last equation back into the definition of :math:`B` we find

.. math::
   B = C^{(n_f)}(Q^2) \otimes E^{(n_f)}(Q^2 \leftarrow m^2) \otimes K^{-1}(1) \otimes E^{(n_f+1)}(m^2 \leftarrow Q^2)

by using the transitive relation of |EKO|. Now, since any |EKO| :math:`E(Q_1^2\leftarrow Q_0^2)` may only depend on
:math:`\log(Q_1^2/Q_0^2)` (it is exactly resumming that log!) :math:`B` can not depend on the matching scale :math:`\mu^2`.

Note, that while nor :math:`C^{(n_f)}` nor :math:`B` may depend on the matching scale, ``yadism`` still has a dependency on the
matching scale: this scales decides which quark to actually treat in the |FONLL| prescription.
Moreover, the physical observable (i.e. the |FK| table) still depends on the matching scale as it simply
inherits the dependency from the evolution (which has an explicit, higher-order dependency on the matching scale).
