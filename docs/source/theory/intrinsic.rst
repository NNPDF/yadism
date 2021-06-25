Heavy-Initiated Contributions (Intrinsic)
=========================================

.. todo:: clarify normalization in a_s


FONLL
~~~~~

.. todo::

   write about the cancellation and then :math:`K_{ij}` use for FONLL in intrinsic
   charm

.. math::

    K_{hh}^{(0)}(Q^2/m_h^2) &= 1\\
    K_{hh}^{(1)}(Q^2/m_h^2) &= 2\left(\bar P_{qq}^{(0)}(z) \left(\ln\left(\frac{Q^2}{m_h^2 (1-z)^2}\right) - 1\right)\right)_+\\
    K_{hg}^{(0)}(Q^2/m_h^2) &= 0\\
    K_{hg}^{(1)}(Q^2/m_h^2) &= 2 P_{qg}^{(0)}(z) \ln\left(\frac{Q^2}{m_h^2}\right)\\
    K_{hg}^{(0)}(Q^2/m_h^2) &= 0\\
    K_{hg}^{(1)}(Q^2/m_h^2) &= 2 P_{gq}^{(0)}(z) \left(\ln\left(\frac{Q^2}{m_h^2 z^2}\right) - 1 \right)

The :math:`K_{ij}` are always relative to the matching threshold, not to the
mass itself.

Nevertheless the effect of choosing an arbitrary threshold :math:`\mu^2`
different from the mass :math:`m^2` is only the appearance in :math:`K_{ij}` of
an extra term proportional to the splitting functions :math:`P_{ij}`:

.. math::

   K_{ij}^{(1)}(\mu^2) = K_{ij}^{(1)}(m^2) + \log(\frac{\mu^2}{m^2}) P_{ij}^{(0)}

see :eqref:`22`, :cite:`nnpdf-intrinsic`.
