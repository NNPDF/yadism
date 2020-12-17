Structure Functions
===================

The |DIS| structure functions are organized in the following way:

- different **kinds** of structure functions, determined by the process external
  kinematics (and so the classification applies to all perturbative orders):
  - unpolarized: F1, F2, F3 
  - polarized: g1, g2, g3, g4, g5 (these are not computed in `yadism`)
- the **heavyness**: there is always one structure function per *kind*
  available, i.e. the *total* one, but based on the *kind* definition more
  observables may be defined
- the **process**: the coefficient functions are computed at |LO| |EW|, and they are organized
according the |EW| boson involved.

Heavyness
~~~~~~~~~

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

Mass corrections
~~~~~~~~~~~~~~~~

The mass corrections (heavy quark contributions) are available for a single
mass at a time, so e.g. `yadism` it is not encoding the effect of having finite
charm and bottom masses at the same time.

The actual scheme is the following:

- :math:`n_l` light flavors are active (i.e. massless quarks)
- a **single** quark with a **finite mass** *may be* active, according to the
  |FNS| (e.g. in ZM-VFNS it will never be such an object)
- all the remaining flavors are considered infinitely massive, so they will
  never contribute to anything

In a |VFNS| this scheme will depend on the specific value of :math:`Q^2`
considered.

