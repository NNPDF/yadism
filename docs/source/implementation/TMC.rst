Target Mass Corrections
=======================

In deep-inelastic lepton-hadron scattering (DIS), when the target hadron has a finite non-zero mass :math:`M`, target mass corrections (TMC) must be taken into account, especially in the kinematic region of low :math:`Q^2` and moderate-to-large Bjorken :math:`x`.

`yadism` provides a complete implementation of target mass corrections for unpolarized structure functions (:math:`F_2`, :math:`F_L`, :math:`F_3`) as well as polarized structure functions (:math:`g_1`) in :mod:`yadism.esf.tmc`.

Kinematics & Nachtmann Variable
-------------------------------

Target mass corrections are formulated in terms of the Nachtmann scaling variable :math:`\xi` and kinematic invariants :cite:`tmc-georgi,Schienbein:2007gr`:

.. math::

   \mu = \frac{M^2}{Q^2}, \qquad \rho = \sqrt{1 + 4 x^2 \mu}, \qquad \xi = \frac{2 x}{1 + \rho}

where :math:`M` is the target mass (defined in the theory card by ``MP``), :math:`x` is the standard Bjorken scaling variable, and :math:`Q^2` is the boson virtuality. Notice that in the massless limit :math:`M \to 0`, :math:`\rho \to 1` and :math:`\xi \to x`.

Target mass corrected structure functions :math:`F^{\rm TMC}(x, Q^2)` are expressed in terms of the "bare" (massless target) structure functions :math:`F(\xi, Q^2)` evaluated at the shifted kinematic scale :math:`\xi`, along with integral convolutions over the structure functions.

TMC Options
-----------

In `yadism`, the target mass correction scheme is configured in the theory dictionary via the ``TMC`` flag:

- **TMC: 0 (Disabled)**:
  No target mass corrections are applied. The bare structure functions are computed directly at :math:`(x, Q^2)`.

- **TMC: 1 (APFEL)**:
  The formulation used historically in APFEL :cite:`nnpdf-1.0`. For :math:`F_2` and :math:`F_L`, the leading integral :math:`h_2` is included while the nested integral :math:`g_2` is neglected (:math:`g_2 = 0`). For :math:`F_3`, since no nested integral exists, APFEL is identical to the exact expression.

- **TMC: 2 (Approximate)**:
  Stemming from :cite:`Schienbein:2007gr,Goharipour:2020gsw`. The integrals appearing in the exact Georgi-Politzer formulas are approximated by evaluating the integrand at the lower limit :math:`\xi`. This eliminates the need for numeric convolution over the :math:`x`-grid, providing substantial computational speedup while maintaining excellent numerical agreement with the exact formulation across the relevant kinematic domain.

- **TMC: 3 (Exact)**:
  The full Georgi-Politzer expressions :cite:`tmc-georgi,Schienbein:2007gr,Goharipour:2020gsw`, incorporating both the shifted bare structure function, the single integral :math:`h_2` (or :math:`h_3`), and the nested integral :math:`g_2`.

Formulas by Observable
----------------------

Structure Function :math:`F_2`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For :math:`F_2`, the exact TMC expression implemented in :class:`~yadism.esf.tmc.ESFTMC_F2` is:

.. math::

   F_2^{\rm TMC}(x, Q^2) = \frac{x^2}{\xi^2 \rho^3} F_2(\xi, Q^2) + \frac{6 \mu x^3}{\rho^4} h_2(\xi, Q^2) + \frac{12 \mu^2 x^4}{\rho^5} g_2(\xi, Q^2)

where the integrals :math:`h_2` and :math:`g_2` are defined as:

.. math::

   h_2(\xi, Q^2) = \int_\xi^1 \frac{du}{u^2} F_2(u, Q^2), \qquad g_2(\xi, Q^2) = \int_\xi^1 du \frac{u - \xi}{u^2} F_2(u, Q^2)

- In the **APFEL** scheme (``TMC = 1``), :math:`g_2` is dropped (:math:`g_2 = 0`).
- In the **Approximate** scheme (``TMC = 2``), the integrals are approximated analytically:

  .. math::

     F_2^{\rm approx}(x, Q^2) = \frac{x^2}{\xi^2 \rho^3} \left[ 1 + \frac{6 \mu x \xi}{\rho} (1 - \xi)^2 \right] F_2(\xi, Q^2)

Longitudinal Structure Function :math:`F_L`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For :math:`F_L`, implemented in :class:`~yadism.esf.tmc.ESFTMC_FL`, the exact expression is:

.. math::

   F_L^{\rm TMC}(x, Q^2) = \frac{x^2}{\xi^2 \rho} F_L(\xi, Q^2) + \frac{4 \mu x^3}{\rho^2} h_2(\xi, Q^2) + \frac{8 \mu^2 x^4}{\rho^3} g_2(\xi, Q^2)

- In the **APFEL** scheme (``TMC = 1``), :math:`g_2` is set to 0.
- In the **Approximate** scheme (``TMC = 2``), the correction terms are approximated via:

  .. math::

     F_L^{\rm approx}(x, Q^2) = \frac{x^2}{\xi^2 \rho} F_L(\xi, Q^2) + \Delta F_L^{\rm approx}(\xi, Q^2)

  where:

  .. math::

     \Delta F_L^{\rm approx}(\xi, Q^2) = \frac{x^2}{\xi^2 \rho} \left[ \frac{4 \mu x \xi}{\rho} (1 - \xi) + 8 \left(\frac{\mu x \xi}{\rho}\right)^2 (-\log \xi - 1 + \xi) \right] F_2(\xi, Q^2)

Structure Function :math:`F_3`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For parity-violating structure function :math:`x F_3`, implemented in :class:`~yadism.esf.tmc.ESFTMC_F3`:

.. math::

   x F_3^{\rm TMC}(x, Q^2) = \frac{x^2}{\xi^2 \rho^2} \xi F_3(\xi, Q^2) + \frac{2 \mu x^3}{\rho^3} h_3(\xi, Q^2)

where the single integral :math:`h_3` is given by:

.. math::

   h_3(\xi, Q^2) = \int_\xi^1 \frac{du}{u} F_3(u, Q^2)

Since there is no second nested integral for :math:`F_3`, the APFEL formulation coincides identically with the exact formula. The approximate scheme (``TMC = 2``) evaluates:

.. math::

   x F_3^{\rm approx}(x, Q^2) = \frac{x^2}{\xi^2 \rho^2} \left[ 1 - \frac{\mu x \xi}{\rho} (1 - \xi) \log \xi \right] \xi F_3(\xi, Q^2)

Polarized Structure Function :math:`g_1`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the spin-dependent structure function :math:`g_1`, implemented in :class:`~yadism.esf.tmc.ESFTMC_g1` following :cite:`Accardi:2008pc,Khanpour:2017cha`:

.. math::

   g_1^{\rm TMC}(x, Q^2) = \frac{x}{\xi \rho^3} g_1(\xi, Q^2) + \frac{4 \mu x^2}{\rho^4} \left[ \frac{x + \xi}{2 \xi} k_1(\xi, Q^2) + \frac{\rho^2 - 3}{4 \rho} k_2(\xi, Q^2) \right]

where:

.. math::

   k_1(\xi, Q^2) = \int_\xi^1 \frac{du}{u^2} g_1(u, Q^2), \qquad k_2(\xi, Q^2) = \int_\xi^1 \frac{du}{u^2} \log\left(\frac{u}{\xi}\right) g_1(u, Q^2)

In the APFEL formulation (``TMC = 1``), the :math:`k_2` term is omitted, while the approximate formulation (``TMC = 2``) approximates the integrals at the lower boundary.

Software Architecture
---------------------

Target mass corrections in `yadism` are designed to integrate cleanly with the structure function caching and interpolation machinery:

1. **Hierarchy and Caching**:
   :class:`~yadism.sf.StructureFunction` acts as the manager. When ``TMC != 0`` in the theory card, it instantiates :class:`~yadism.esf.tmc.EvaluatedStructureFunctionTMC` subclasses (mapped via :data:`~yadism.esf.tmc.ESFTMCmap`) rather than standard :class:`~yadism.esf.esf.EvaluatedStructureFunction`.

2. **Integration on Interpolation Grids**:
   When evaluating integral convolutions (:math:`h_2`, :math:`g_2`, :math:`h_3`, :math:`k_1`, :math:`k_2`), :meth:`~yadism.esf.tmc.EvaluatedStructureFunctionTMC._convolve_FX` convolving the kernel with the structure function over the interpolation polynomial grid:

   .. math::

      \tilde{F}_X \otimes f = \sum_{i,j} F_X(x_j) \cdot (w_j \otimes k)(\xi) \cdot f(x_i)

   where :math:`w_j` are interpolation basis polynomials, postponing contraction with PDFs until the final stage.

3. **Routing to Siblings**:
   When computing :math:`F_L^{\rm TMC}`, which requires integrals over :math:`F_2`, the instance requests the corresponding :math:`F_2` from its parent manager via :meth:`~yadism.sf.StructureFunction.get_esf`, ensuring cached evaluations are reused.

4. **Result Tagging**:
   Although intermediate calculations evaluate bare structure functions at the shifted scale :math:`\xi`, the returned :class:`~yadism.esf.result.ESFResult` object is explicitly tagged with the physical kinematics :math:`(x, Q^2)`.

Recent Developments & Nuclear DIS
---------------------------------

For comprehensive reviews of target mass corrections, see :cite:`Schienbein:2007gr` and :cite:`Goharipour:2020gsw`. Applications to lepton-nucleus deep-inelastic scattering and nuclear PDFs, including nuclear target mass corrections and their interplay with nuclear shadowing and Fermi motion, are discussed in :cite:`Ruiz:2023fnm`.
