Benchmarks
==========

Benchmarks are implemented against external code, where they overlap with this
package.


|APFEL|
-------

It is a tool aimed to the evolution of PDFs and DIS observables' calculation
(and FTDY as well).

It has been used by the NNPDF collaboration up to NNPDF4.0

|QCDNUM|
--------

It is a tool aimed to the evolution of PDFs and DIS observables' calculation in
a restricted number of schemes.

It is/has been used by the `xFitter` framework.

Different definition of |SF|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to a different definition |SF| in |APFEL| (and so `yadism`) and |QCDNUM| is
not possible to compare all the structure functions in all the schemes.

In particular |APFEL|/`yadism` definition of |SF| is based on the coupling to
the photon (or |DIS| boson in general), cf. :doc:`../theory/light-flavors` and
:doc:`../theory/heavy-flavors`.

On the other hand |QCDNUM| is using a different definition of the |SF| that is
not matching the other one and from which it is not possible to recover the
other results at higher orders (in particular it becomes completely impossible
since |NNLO|).
The different definition is:

- :math:`F_X^{light}` is defined by having only light quarks in the quark lines
- :math:`F_X^{charm}` is defined by having light and charm quarks in the
  quark lines (at least one charm), given that charm is not light (otherwise
  it's not defined) 
- and so on for :math:`bottom` (that will include at least one bottom) and
  :math:`top` (that will include at least one top)
