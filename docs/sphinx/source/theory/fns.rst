Flavor Number Schemes
=====================

FFNS
----

The mass corrections (heavy quark contributions) are available for a single
mass at a time, so e.g. `yadism` it is not encoding the effect of having finite
charm and bottom masses at the same time.

The actual scheme is the following:

- :math:`n_l` light flavors are active (i.e. massless quarks)
- a **single** quark with a **finite mass** *may be* active, according to the
  |FNS| (e.g. in ZM-VFNS it will never be such an object)
- all the remaining flavors are considered infinitely massive, so they will
  never contribute to anything

ZM-VFNS
-------

In a |VFNS| this scheme will depend on the specific value of :math:`Q^2`
considered.

FONLL
-----

TODO OLD STUFF
--------------
.. todo:: rewrite this


Heavyness
---------

There is always a lot of ways to define physical observables, e.g. tagging the
outgoing state and imposing kinematics cuts.

We are not going to use any definition based on the outgoing state, since they
are prone to be theoretically unsafe, if not properly designed.

The way we are defining new observables it is just considering new theories,
derived from the |SM| just setting to 0 some of its bare couplings.

- **Flight**: it is defined as the original structure function (e.g.
  :math:`F_2`) for the theory in which all the *light* quarks are massless, and
  all the *heavy* ones are infinitely massive, such that they are never
  contributing to the diagrams
- **Fheavy**: it is defined for a given flavor, e.g. *Fcharm*, just keeping
  all the *light* quark massless, a finite mass for a single heavy quark (the
  one associated to the structure function chosen) and all the others *heavy*
  infinitely massive, switching to 0 all the charges that do not involve the
  chosen heavy quark

  - in |NC| this means that only the *charm* charge is kept
  - in |CC| this means that :math:`V_{cd}` and :math:`V_{cs}` are kept, but e.g.
    there is no contribution by :math:`V_{cb}`, because currently bottom is
    considered infinitely massive

    - we could also define by arbitrarily assign CKM matrix elements to a single
      flavor, choosing always the heaviest, and set to 0 all the things not
      assigned to the chosen flavor, it is just an equivalent way of presenting
      it

No other observable than **Flight**, **Fheavy**, **Ftotal** (for all the
unpolarized *kinds*) and **sigma** is provided by `yadism`.



- References

.. _heavy-nc:

NC
--

The main reference is :cite:`felix-thesis`.

- meanings of :math:`F_2^{charm}` (c coupling to |EW| boson) (and analogously
  for `bottom` and `top`)

.. _heavy-cc:

CC
--

The main reference is :cite:`gluck-ccheavy`.

- meanings of :math:`F_2^{charm}` (the weight coming from the suitable line of
  the CKM matrix) (and analogously for `bottom` and `top`)

.. math::
   V_{CKM} =
   \begin{pmatrix}
      {\color{red}V_{ud}} & {\color{red}V_{us}} & {\color{green}V_{ub}}\\
      {\color{blue}V_{cd}} & {\color{blue}V_{cs}} & {\color{green}V_{cb}}\\
      {\color{purple}V_{td}} & {\color{purple}V_{ts}} & {\color{purple}V_{tb}}
   \end{pmatrix}

actual definition of coefficient functions weights in :math:`F_2` (with an
initial neutrino, :math:`\nu`):

.. math::
   \begin{array}{rcl}
      F_2^{\nu,p} &=& 2x\Big\{C_{2,q}\otimes
                  \Big[\left(|{\color{red}V_{ud}}|^2+|{\color{blue}V_{cd}}|^2+|{\color{purple}V_{td}}|^2\right)d\\
                  &+&
                  \left(|{\color{red}V_{ud}}|^2+|{\color{red}V_{us}}|^2+|{\color{green}V_{ub}}|^2\right)\overline{u}\\
                  &+&
                  \left(|{\color{red}V_{us}}|^2+|{\color{blue}V_{cs}}|^2+|{\color{purple}V_{ts}}|^2\right)s\\
                  &+&
                  \left(|{\color{blue}V_{cd}}|^2+|{\color{blue}V_{cs}}|^2+|{\color{green}V_{cb}}|^2\right)\overline{c}\\
                  &+&
                  \left(|{\color{green}V_{ub}}|^2+|{\color{green}V_{cb}}|^2+|{\color{purple}V_{tb}}|^2\right)b\\
                  &+&
                  \left(|{\color{purple}V_{td}}|^2+|{\color{purple}V_{ts}}|^2+|{\color{purple}V_{tb}}|^2\right)\overline{t}\Big]\\
                  &+& c^{CC}_g(N_f)C_{2,q}\otimes g\Big\}
   \end{array}

and in :math:`F_2^{charm}`:

.. math::
   {\color{blue} F_{2,c}^{\color{black} \nu,p}} &=& 2x\Big\{C_{2,q}\otimes\Big[|{\color{blue}V_{cd}}|^2(d+\overline{c}) +
         |{\color{blue}V_{cs}}|^2 (s+\overline{c})\Big]\\
         &+& 2\left(|{\color{blue}V_{cd}}|^2+|{\color{blue}V_{cs}}|^2\right)C_{2,g}\otimes g\Big\}\\

.. todo:: write about normalization in Eq. 2

Asymptotics for FONLL
~~~~~~~~~~~~~~~~~~~~~
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

