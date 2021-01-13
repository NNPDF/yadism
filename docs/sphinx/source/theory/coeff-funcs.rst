Coefficient Functions
=====================

Overview of coefficient functions structure
-------------------------------------------

The main categories for coefficients the same of Structure Functions, i.e.:

- the **process** (EM/NC/CC)
- the **kind** (F2/L/3)
- the **heavyness** involved (light/charm/bottom/top/total)
- but there is a new one: the **channel** (ns/ps/g), and it is related to the
  incoming parton:

  - if the |EW| boson it is coupling to a *quark* line connected to the incoming
    one, than each PDF it's contributing proportionally to his charge (e.g.:
    electric charge for the photon); this is called **non-singlet (ns)**
  - otherwise the line to which the |EW| boson is coupling it will be detached
    from the incoming  by *gluonic* lines, and the gluon is flavor blind, so
    all the charges are summed and all the PDF are contributing the same way;
    this is called **pure singlet (ps)**
  - eventually: if a *gluon* is entering all the quarks will couple to the |EW|
    boson (if no further restrictions are imposed by the observable, e.g.
    F2charm), as in the singlet case, and so the charges are summed over; this
    is called the **gluon (g)** (because *it is* the gluon...)
  - the **parity structure** (vectorial-vectorial/axial-axial/vectorial-axial),
    it is relevant only for the NC, and should be taken into account

These options set the overall structure of the coefficient functions, and it is
reported in the following tables, just considering that the mass corrections
for all the  flavors (charm/bottom/top) share the same functional form for the
coefficient and a further category (the massless limit of the heavy) is needed
for variable flavor scheme like FONLL.

.. csv-table:: NC coefficients
   :file: ./nc-coeffs.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center


.. csv-table:: CC coefficients
   :file: ./cc-coeffs.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center

Distributions
-------------

To obtain a physical observable one has to convolute the coefficient functions with the |PDF|

.. math ::
    \sigma = \sum_j f_j \otimes c_j = \sum_j \int\limits_x^1 \frac {dz}{z} f_j(x/z) c_j(z)


A generic coefficient function will allow for three ingredients:

- Regular functions :math:`r(z)` that are well behaving, i.e. integrable,
  for all :math:`z \in (0,1]`; these typically contain polynomials, logarithms
  and dilogarithms
- Dirac-delta distributions: :math:`\delta(1-z)`
- Plus distributions: :math:`\left[g(z)\right]_+` which have a regulated singularity at :math:`z\to 1`
  and are defined by

.. math ::
  \int\limits_0^1 \!dz\, f(z) \left[g(z)\right]_+ = \int\limits_0^1\!dz\, \left(f(z) - f(1)\right)g(z)

The "plused" function can be a generic function, but in practice will almost always be :math:`\log^k(1-z)/(1-z)`.
The "plused" function has to be regular at :math:`z=0`. These contributions are related to soft and/or
collinear singularities in the physical process.

In order to do the convolution in a generic way we adopt the |RSL| scheme:
i.e. we categorize them by their behavior under the convolution interal. This is needed because
of the mismatch in the definitions of the convolution and the plus prescription.
Any coefficient function :math:`c(z)` can be written in the following way:

.. math ::
  f \otimes c = \int\limits_x^1 \! \frac{dz}{z} \, f(x/z) c^R(z) + \int\limits_x^1 \! dz \, \left(\frac{f(x/z)}{z} - f(x)\right) c^S(z) + f(x) c^L(x)

The remapping of the coefficient function ingredients on to the |RSL| elements is done in the
following way:

- Regular functions :math:`c(z) = r(z)` contribute only to the regular bit:

.. math ::
  c^R(z) = r(z)\,,~ c^S(z) = 0 = c^L(x)

- Dirac delta distributions :math:`c(z) = \delta(1-z)` only contribute to the local bit:

.. math ::
  c^R(z) = 0 = c^S(z)\,,~ c^L(x) = 1

- "Raw" plus distributions :math:`c(z) = \left[g(z)\right]_+` contribute to both the singular
  and the local bit:

.. math ::
  c^R(z) = 0\,,~ c^S(z) = g(z)\,,~ c^L(x) = \int_0^x\!dz\, g(z)

.. details :: derivation

  .. math ::
    f \otimes [g]_+ &= \int_x^1 \frac{dz}{z} f(x/z) \cdot \left[ g(z) \right]_+\\
    &= \int_0^1 \frac{dz}{z} f(x/z) \cdot \left[ g(z) \right]_+ - \int_0^x \frac{dz}{z} f(x/z) \cdot \left[ g(z) \right]_+\\
    &= \int_0^1\!dz\, \left(\frac{f(x/z)}{z} - f(x)\right) \cdot g(z) - \int_0^x\!dz\, \frac{f(x/z)}{z} \cdot g(z)\\
    &= \int_x^1\!dz\, \left(\frac{f(x/z)}{z} - f(x)\right) \cdot g(z) - f(x) \int_0^x\!dz\, g(z)\\
    &\Rightarrow c^R(z) = 0, c^S(z) = g(z), c^L(x) = \int_0^x\!dz\, g(z)

- Finally a product of a regular function and a plus distribution :math:`c(z) = g(z)\left[h(z)\right]_+`
  contributes to all three bits:

.. math ::
  c^S(z) = g(1)h(z)\,,~ c^R(z) = (g(z)-g(1))h(z)\,,~  c^L(x) = g(1)\int_0^x\!dz\, h(z)

.. details :: derivation

  .. math ::
      f\otimes c &= \int_x^1 \frac{dz}{z} f(x/z) g(z) \cdot \left[ h(z) \right]_+\\
      &= \int_0^1 \frac{dz}{z} f(x/z) g(z) \cdot \left[ h(z) \right]_+ - \int_0^x \frac{dz}{z} f(x/z) g(z) \cdot \left[ h(z) \right]_+\\
    &= \int_0^1 dz \left(\frac{f(x/z)g(z)}{z} - f(x)g(1)\right) \cdot h(z) - \int_0^x\!dz\, \frac{ f(x/z) g(z)}{z} \cdot h(z)\\
    &= \int_x^1 dz \left(\frac{f(x/z)g(z)}{z} - f(x)g(1)\right) \cdot h(z) - f(x) g(1) \int_0^xdz~ h(z)\\
    &= \int_x^1 dz \left(\frac{f(x/z)(g(z)+g(1)-g(1))}{z} - f(x)g(1)\right) \cdot h(z) - f(x) g(1) \int_0^xdz~ h(z)\\
    &= \int_x^1 dz \left(\frac{f(x/z)}{z} - f(x)\right)  g(1)\cdot h(z) + \int_x^1 dz \frac{f(x/z)(g(z)-g(1)))}{z} h(z)  - f(x) g(1) \int_0^xdz~ h(z)\\
    &= \int_x^1  \frac{dz}{ z} f(x/z)  g(1)\cdot \left[h(z)\right]_+ + \int_x^1 dz \frac{f(x/z)(g(z)-g(1)))}{z} h(z)\\
    &\Rightarrow c^S(z) = g(1)h(z), c^R(z) = (g(z)-g(1))h(z),  c^L(x) = g(1)\int_0^x\!dz\, h(z)
