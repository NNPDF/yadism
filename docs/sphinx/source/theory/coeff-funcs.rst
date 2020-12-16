Coefficient Functions
=====================

Overview of coefficient functions structure
-------------------------------------------

The main categories for coefficients the same of :doc:`structure-functions`, i.e.:

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

- Regular functions that are well behaving, i.e. integrable, for all :math:`z \in (0,1]`
- Dirac-delta distributions: :math:`\delta(1-z)`
- Plus distributions: :math:`\left[f(z)\right]_+` which are defined by

.. math ::
  \int\limits_0^1 \dz g(z) \left[f(z)\right]_+ = \int\limits_0^1 \left(g(z) - g(1)\right)f(z)

The "plused" function can be a generic function, but in practice will almost always be :math:`\log^k(1-x)/(1-x)`.
The "plused" function has to be regular at :math:`z=0`.

In order to do the convolution in a generic way we adopt the Regular-Singular-Local scheme (RSL):
i.e. we categorize them by their behavior under the convolution interal. This is needed because of the mismatch in the
definitions of the convolution and the plus prescription.


Convolution to Integration
""""""""""""""""""""""""""

.. math::

   \begin{align}
   \int_x^1 \frac{\text{d} z}{z} f(z) \cdot \left[ h(z) \right]_+ &=
   \int_0^1 \frac{\text{d} z}{z} f(z) \cdot \left[ h(z) \right]_+ - \int_0^x \frac{\text{d}
   z}{z} f(z) \cdot \left[ h(z) \right]_+\\
   &= \int_0^1 \text{d} z \left(\frac{f(z)}{z} - f(1)\right) \cdot h(z) - \int_0^x \text{d}
   z \frac{ f(z)}{z} \cdot h(z)\\
   &= \int_x^1 \text{d} z \left(\frac{f(z)}{z} - f(1)\right) \cdot h(z) - f(1) \int_0^x
   \text{d} z~ h(z)
   \end{align}

And explicitly for a product of distributions:

.. math::

   \begin{align}
    & \int_x^1 \frac{\text{d} z}{z} f(z) g(z) \cdot \left[ h(z) \right]_+\\
    &=
   \int_0^1 \frac{\text{d} z}{z} f(z) g(z) \cdot \left[ h(z) \right]_+ - \int_0^x \frac{\text{d}
   z}{z} f(z) g(z) \cdot \left[ h(z) \right]_+\\
   &= \int_0^1 \text{d} z \left(\frac{f(z)g(z)}{z} - f(1)g(1)\right) \cdot h(z) - \int_0^x \text{d}
   z \frac{ f(z) g(z)}{z} \cdot h(z)\\
   &= \int_x^1 \text{d} z \left(\frac{f(z)g(z)}{z} - f(1)g(1)\right) \cdot h(z) - f(1) g(1) \int_0^x\text{d} z~ h(z)\\
   &= \int_x^1 \text{d} z \left(\frac{f(z)(g(z)+g(1)-g(1))}{z} - f(1)g(1)\right) \cdot h(z) - f(1) g(1) \int_0^x\text{d} z~ h(z)\\
   &= \int_x^1 \text{d} z \left(\frac{f(z)}{z} - f(1)\right)  g(1)\cdot h(z) + \int_x^1 \text{d} z \frac{f(z)(g(z)-g(1)))}{z} h(z)  - f(1) g(1) \int_0^x\text{d} z~ h(z)\\
   &= \int_x^1  \frac{\text{d} z}{ z} f(z)  g(1)\cdot \left[h(z)\right]_+ + \int_x^1 \text{d} z \frac{f(z)(g(z)-g(1)))}{z} h(z)
   \end{align}


Regular - Singular - Local (RSL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first one can be integrated by ordinary methods, but the other two will
deserve special care:

- the :math:`delta` part it becomes a simple evaluation of anything multiplied,
  but since this is not going to be numerically integrated this contributions
  are split in the code and directly evaluated; this *not-integrated* part is
  called the **local (L)** part, and :math:`delta` contributions will go
  completely into it
- the plus distributions instead will contribute to two different parts: the
  *local* and the **singular (S)** one, that it will involve an integration
  with not just the plain function multiplied to it, but a little bit more
  complicate prescription, i.e.:

.. math::

   \int_x^1 \frac{\text{d} z}{z} f(z) \cdot \left[ h(z) \right]_+ = \int_x^1
   \text{d} z \left(\frac{f(z)}{z} - f(1)\right) \cdot h(z) - f(1) \int_0^x
   \text{d} z~ h(z)

.
   as it is derived in the previous section; the first bit will be the plus
   distribution contribution to the *singular*, while the second to the *local*
   part of the integration

