Heavy Flavors
=============

.. _heavy-nc:

NC
--

The main reference is :cite:`felix-thesis`.

.. _heavy-cc:

CC
--

The main reference is :cite:`gluck-ccheavy`.

.. todo:: write about normalization in Eq. 2

Asymptotics for FONLL
~~~~~~~~~~~~~~~~~~~~~

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


Flavor Number Schemes
---------------------

- FFNS
- ZM-VFNS

.. _asymptotic:

FONLL
~~~~~
  
- Damping
