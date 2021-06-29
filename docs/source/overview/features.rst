Features
=========

``yadism`` implements the |DIS| observables up to |NNLO|, i.e. it is possible to
ask for the following perturbative orders:

- |LO|
- |NLO|
- |NNLO|

The implemented observables consist of:

- the |DIS| unpolarized :ref:`structure functions
  <theory/intro:structure function kind>`: :math:`F_2`, :math:`F_L`, and
  :math:`F_3` (the structure function :math:`F_1` is not directly provided)
- the |DIS| reduced :ref:`cross sections <theory/intro:cross sections>`
  (with various normalizations)

for all the possible |EW| bosons, i.e. for the :ref:`processes
<theory/intro:process / currents>`: |EM|, |NC|, |CC|.

All the observables are delivered both as their total value, but also split up
according to their :ref:`heavyness <theory/intro:Heavyness>` (e.g.
:math:`F_{2,c}` is provided).

Moreover the following features are all available:

1. :doc:`flavor number schemes <../theory/fns>`: |FFNS|, |ZM-VFNS|, |FONLL|
2. :doc:`scale variations <../theory/scale-variations>`: independent variations
   of factorization scale :math:`\mu_F` and renormalization scale :math:`\mu_R`
3. :ref:`target mass corrections <theory/misc:target mass corrections>`
   (available with the exact numerical integration and as approximate
   non-integrated expressions)
4. :doc:`intrinsic flavors <../theory/intrinsic>`, i.e. heavy quark-initiated |DIS|
