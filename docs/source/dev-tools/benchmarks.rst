Benchmarks
==========

Benchmarks are implemented against external code, where they overlap with `yadism`.
Benchmarks are implemented using an independent package called `yadmark` described
in the relative section.

We compare `yadism` with three external tools: |APFEL|, |QCDNUM| and |xspace-bench|,
which are described in details below.

Different definition of |SF|
----------------------------

Due to a different definition |SF| in `yadism`, |APFEL|, |QCDNUM| and |xspace-bench| it is
not possible to compare all the structure functions in all the schemes.

.. important::

   For the actual definition of |SF| in `yadism` (which is of course |FNS|
   dependent) look at :doc:`../theory/fns` section.

The following tables summarize the possible combination of benchmarks, including
also incoming projectiles, different type of currents, SV and TMC.

.. csv-table:: Flavor Number Schemes
   :file: ./bench-fns.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center

.. [#f1] Only for NfFF=3

.. csv-table:: Banchmarks coverage
   :file: ./bench-coverage.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center


APFEL
-----

|APFEL| is a tool aimed to the evolution of PDFs and DIS observables' calculation
(and FTDY as well).

It has been used by the NNPDF collaboration up to NNPDF4.0

SF in APFEL
~~~~~~~~~~~

The |APFEL| definitions are such that the following relation always holds:

.. math::

   F_X^{total} = F_X^{light} + F_X^{charm} + F_X^{bottom} + F_X^{top}


In order to keep this relation the following definitions are adopted:

- :math:`F_X^{light}` is called the hood collecting all the contributions in
  which :math:`u, d, s` quarks are coupling to the |EW| boson and nothing else
- :math:`F_X^{heavy}` are defined as the collections of contributions in which
  only the specified heavy quark it's coupling to the |EW| boson, and they
  account only for the corresponding :math:`m_{heavy}` effects (but not for the
  mixed ones)

These definitions are consistent up to |NNLO|, but they are not easy to apply
to all the |FNS| at higher orders because:

- in the |VFNS| the light quarks are dynamical, so the number of objects
  running in quark loops as well: when this causes a non-linear dependence on
  the number of light flavors :math:`n_l` (e.g. a quadratic one) it is
  difficult (if not impossible) to split up into :math:`F_X^{light}` and not
- since not all the massive contributions are accounted for in the
  proper :math:`F_X^{heavy}` (some of them are collected in
  :math:`F_X^{light}`, or in other heavy ones) these are not well-defined
  observables on their own (from a pure QFT-theoretical point of view), then
  they could not be compared with tagged experimental data
- mixed mass effects are known to be small, but it's rather inconsistent to
  account for certain mass effects that are even smaller in suitable
  :math:`Q^2` regimes and not for them; e.g. charm-bottom interplay may be more
  relevant then top contributions much below top production threshold

QCDNUM
------

|QCDNUM| is a tool aimed to the evolution of PDFs and DIS observables' calculation in
a restricted number of schemes.

It is/has been used by the `xFitter` framework.

SF in QCDNUM
~~~~~~~~~~~~

|QCDNUM| is using a different definition of the |SF| that is not matching the
other one and from which it is not possible to recover the other results at
higher orders (in particular it becomes completely impossible since |NNLO|).
The different definition is:

- :math:`F_X^{light}` is defined by having only light quarks in the quark lines
- :math:`F_X^{charm}` is defined by having light and charm quarks in the
  quark lines (at least one charm), given that charm is not light (otherwise
  it's not defined)
- and so on for :math:`F_X^{bottom}` (that will include at least one bottom) and
  :math:`F_X^{top}` (that will include at least one top)

Only |EM| and |NC| currents are available in |QCDNUM|.

xspace-bench
------------

|xspace-bench| is a tool aimed to the evolution of PDFs and DIS observables' calculation for
|NC| and |CC|, with different type of projectiles and targets. |SF| can be computed up to |NLO|,
and few |FNS| configurations are available, since their settings are hardcoded.

SF in xspace-bench
~~~~~~~~~~~~~~~~~~

In |xspace-bench| |SF| are defined as follows:

- :math:`F_X^{light}` is defined by having only light quarks in the quark lines (u,d,s)
- :math:`F_X^{charm}` is defined by having light and charm quarks in the
  quark lines (at least one charm), given that charm is not light (otherwise
  it's not defined)
- and so on for :math:`F_X^{bottom}` (that will include at least one bottom) and
  :math:`F_X^{top}` (that will include at least one top)
- :math:`F_X^{total}` is defined as the sum of the previous ones.

Given these definitions, benchmarks with `yadism` are possible only in the region
:math:`m^2_{charm} < Q^2 < m^2_{bottom}` selecting  either |ZM-VFNS| with :math:`F_X^{total}`
or |FFNS| with NfFF=3.
FONLL is implemented in the so called `scheme A` with and without damping factor.

APFEL++
-------


|APFEL++| is a C++ rewriting of the Fortran 77 evolution code |APFEL|. However, |APFEL++| is based on a completely new code design and 
guarantees a better performance along with a more optimal memory management. 
|APFEL++| is suitable for a wide range of tasks: from the solution of the DGLAP evolution equations to the computation of DIS
and single-inclusive-annihilation cross sections. 

|APFEL++| is also currently interfaced to PARTONS, a software dedicated to the phenomenology of Generalised Parton Distributions (GPDs) and TMDs, 
and to xFitter.


SF in APFEL++
~~~~~~~~~~~~~

The |APFEL++| definitions follows the one of |APFEL|
