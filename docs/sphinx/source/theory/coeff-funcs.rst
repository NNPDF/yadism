Coefficient Functions Calculation
=================================


Convolution Integral
--------------------

How we recast convolution in an integration in [0,1] (where plus distributions
are properly defined) plus some addends.

Convolution to Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
--------------------------------

A generic coefficient function will allow for three ingredients:

- regular functions
- :math:`delta(1-x)` distributions
- :math:`\left[f(x)\right]_+` distributions (where the function inside can be a
  generic function, but it will always be :math:`\log^k(1-x)/(1-x)` in practice)

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

   as it is derived in the previous section; the first bit will be the plus
   distribution contribution to the *singular*, while the second to the *local*
   part of the integration

Integral Details
----------------

- if area does not overlap it's set to 0 and integral skip
- we are using `scipy.quad`
- precision can be set
- some areas specification are passed to quad
- the extremes are cut a little, to regulate integration behavior
