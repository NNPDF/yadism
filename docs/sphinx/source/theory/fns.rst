Flavor Number Schemes
=====================

|FNS| or Heavy Quark Matching Schemes are dealing with the ambiguity of including
massive quark contributions to physical cross sections. There is is not a unique
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
As the name suggests we are considering a fixed number of flavors :math:`n_f=n_l+1`
with :math:`n_l` light flavors and 1 (and only 1) heavy flavor. The number of light
quarks :math:`n_l` is arbitrary but fixed and can range between 3 and 5.

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

ZM-VFNS
-------

In a |VFNS| this scheme will depend on the specific value of :math:`Q^2`
considered.

FONLL
-----

Asymptotics for CC
^^^^^^^^^^^^^^^^^^
.. todo :: this is simply light as it should! write it

For FONLL we need the massless limit of the coefficient functions in :cite:`gluck-ccheavy`.
We obtain :math:`\lambda\to 1, \xi \to x` and

- **light quark** channel:

.. math::
    H_i^{q,asy} &= P_{qq}(z) \ln (Q^2/\mu_F^2) + h_i^{q,asy}(z)\\
    h_i^{q,asy} &= C_F \left[ -\left(\frac 9 2 + \frac{\pi^2}{3} \right)\delta(1-z) - \frac{1+z^2}{1-z} \ln(z) + (1+z^2)\left( \frac{\ln(1-z)}{1-z}\right)_+ \right.\\
                &\hspace{40pt} + \left. B^{(i)}\left(\frac 1 {1-z}\right)_+  \right]

with :math:`K_A \to 0` and the coefficients :math:`B^{(i)} = B_{1,i} + B_{2,i} + B_{3,i}` given by

.. list-table::
    :stub-columns: 1

    * - :math:`B^{(1)}`
      - :math:`\frac 3 2 - 3 z`
    * - :math:`B^{(2)}`
      - :math:`\frac 3 2 - z - 2z^2`
    * - :math:`B^{(3)}`
      - :math:`\frac 1 2 - z - z^2`

For :math:`F_L = F_2 - 2xF_1` we obtain:

.. math::
    H_L^{q,asy} &= H_2^{q,asy} - H_1^{q,asy} \\
                &= C_F \left(B^{(2)} - B^{(1)}\right)\left(\frac 1 {1-z}\right)_+\\
                &= C_F \cdot 2z

- **gluon** channel:

.. math::
    H_{i=1,2/3}^{g,asy} &= P_{qg}(z)\left(\pm\left(\ln((1-z)/z) + \ln(Q^2/m^2)\right) + \ln (Q^2/\mu_F^2)\right) + h_i^{g,asy}(z)\\
    h_i^{g,asy} &= P_{qg}(z) \ln((1-z)/z) + C_{1,i}^{asy} z(1-z) + C_{2,i}^{asy}

with the coefficients :math:`C_{i,j}^{asy}` given by

.. list-table::
    :header-rows: 1
    :stub-columns: 1

    * - structure function
      - :math:`C_{1,i}^{asy}`
      - :math:`C_{2,i}^{asy}`
    * - :math:`F_1`
      - :math:`4`
      - :math:`-1`
    * - :math:`F_2`
      - :math:`8`
      - :math:`-1`
    * - :math:`F_3`
      - :math:`0`
      - :math:`0`

For :math:`F_L = F_2 - 2xF_1` we obtain:

.. math::
    H_L^{g,asy} &= H_2^{g,asy} - H_1^{g,asy} \\
                &= \left(C_{1,2}^{asy} - C_{1,1}^{asy}\right) z(1-z) + \left(C_{2,2}^{asy} - C_{2,1}^{asy}\right)\\
                &= 4z(1-z)

