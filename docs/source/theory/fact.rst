Factorization
=============

.. figure:: /_static/dis-hadronic-leptonic.svg
   :align: center

   In blue the leptonic coupling, the corresponding green one, close to the
   blob, is instead the hadronic coupling.
   The blob itself is the hadronic contribution.

We refer to Factorization as the universal property that the |DIS| cross section
can be factored into different parts: **DIS Factorization** ensures that
the cross section can be split into a *leptonic* and an *hadronic* part.
In *addition* on the hadronic part **Collinear Factorization** ensures that the structure
functions can be split into an perturbative hard matix element and a non-perturbative |PDF|.

In the following we will explain how to connect the top-level observables and the
low-level ingredients using the notation of :cite:`Zyla:2020zbs`.

DIS Factorization
-----------------

The fully inclusive |DIS| cross section :math:`\sigma` is given by

.. math ::
    \frac{d\sigma^i}{dx dy} = \frac{2\pi y \alpha^2}{Q^4} \sum_b \eta_b L^{\mu\nu}_b W_{\mu\nu}^b

where :math:`i \in \{\text{NC}, \text{CC}\}` corresponds to the |NC| or |CC| processes, respectively.
For |NC| processes, the summation is over :math:`b \in \{\gamma\gamma,\gamma Z,ZZ\}`,
whereas for |CC| interactions there is only W exchange :math:`b=\{W\}`.
The normalization factors :math:`\eta_b` denote the ratios of the corresponding propagators and
couplings to the photon propagator and coupling squared:

.. math ::
    \eta_{\gamma\gamma} &= 1\\
    \eta_{\gamma Z} &= \frac{4\sin^2(\theta_w)}{1 - \sin^2(\theta_w)} \cdot \frac{Q^2}{Q^2 + M_Z^2}\\
    \eta_{ZZ} &= \eta_{\gamma Z}^2\\
    \eta_W &= \left(\frac{\eta_{\gamma Z}}{2} \frac{1 + Q^2/M_Z^2}{1 + Q^2/M_W^2}\right)^2

Implementation: :meth:`~yadism.coupling_constants.CouplingConstants.propagator_factor`

The leptonic tensors :math:`L_b^{\mu\nu}` can all be written in terms of the photonic lepton
tensor, because the lepton is assumed massless:

.. math ::
    L^{\gamma\gamma}_{\mu\nu} &= 2\left(k_{\mu}k_{\nu}' + k_{\nu}k_{\mu}' - (k\cdot k') g_{\mu\nu} - i\lambda \epsilon_{\mu\nu\alpha\beta}k^{\alpha}k'^{\beta}\right)\\
    L^{b}_{\mu\nu} &= \kappa_b ~ L^{\gamma}_{\mu\nu}\\
    \kappa_{\gamma Z} &= (g_V^e + e\lambda g_A^e)\\
    \kappa_{ZZ} &= (g_V^e + e\lambda g_A^e)^2\\
    \kappa_{W} &= (1 + e\lambda)^2

with :math:`g_V^e = -\frac 1 2 + 2\sin^2(\theta_w)` and :math:`g_A^e = -\frac 1 2` the vectorial
and axial-vectorial coupling between the Z boson and the lepton with charge :math:`e=\pm 1` and
helicity :math:`\lambda=\pm 1`.

For the unpolarized scattering, the hadronic tensor is given by:

.. math ::
    W_{\mu\nu} = \left(-g_{\mu\nu} + \frac{q_\mu q_\nu}{q^2}\right) F_1(x,Q^2)
                + \frac{\hat P_\mu \hat P_\nu}{P \cdot q} F_2(x,Q^2)
                - i \varepsilon_{\mu\nu\alpha\beta} \frac{q^\alpha P^\beta}{2 P\cdot q} F_3(x,Q^2)

Inserting the leptonic and the hadronic tensors into the cross section we obtain

.. math ::
    \frac{d\sigma^i}{dx dy} = \frac{4\pi \alpha^2}{x y Q^2} \eta^i \left\{
    \left(1-y - \frac{x^2 y^2 M^2}{Q^2}\right)F_2^i
    + y^2 x F_1^i
    \pm \left(y - \frac {y^2}{2} \right) x F_3^i
    \right\}

where the :math:`-` sign in front of :math:`F_3` is taken for an incoming :math:`e^+`
or :math:`\bar \nu` and the :math:`+` sign for an incoming :math:`e^-` or :math:`\nu`.
The normalization factor :math:`\eta^i` are given by :math:`\eta^{NC} = 1` and
:math:`\eta^{CC} = \kappa_W \eta_W`. So unlike in the |NC| process, in the |CC| process
the leptonic couplings and the propagator corrections are *not* inside the structure functions
but enter only on a cross section level. This is possible because in |CC| there are no
interferences between different bosons. The structure functions are given by

.. math ::
    F_k^{CC} &= F_k^W\\
    F_k^{NC} &= F_k^{\gamma\gamma} - (g_V^e \pm \lambda g_A^e) \eta_{\gamma Z} F_k^{\gamma Z} + \left((g_V^e)^2 + (g_A^e)^2  \pm 2 \lambda g_V^e g_A^e \right) \eta_{ZZ} F_k^{ZZ}~,~ k\in\{1,2,L\} \\
    x F_3^{NC} &= -(g_A^e \pm g_V^e) \eta_{\gamma Z} x F_3^{\gamma Z} + \left(2g_V^e g_A^e \pm \lambda((g_V^e)^2 + (g_A^e)^2)\right) x F_3^{ZZ}

Implementation: :meth:`~yadism.coupling_constants.CouplingConstants.leptonic_coupling`.

Similar decompositions holds also in the polarized |DIS|, where the hadronic tensor :math:`W_{\mu\nu}`
can be decomposed to other basic structure functions called :math:`g_4,g_L,g_1`.

Collinear Factorization
-----------------------

Using the collinear factorization theorem of |DIS| :cite:`Collins:1989gx` we can write any
hadronic structure function :math:`F_k` in terms of |PDF| :math:`f_j(\xi,\mu_F^2)` and
partonic structure functions :math:`\mathcal F_{j,k}(z, Q^2,\mu_F^2,\mu_R^2)` using a convolution
over the first argument:

.. math ::
    F_k^{bb'}(x,Q^2,\mu_F^2,\mu_R^2) = \sum_{p} f_p(\mu_F^2) \otimes \mathcal F_{k,p}^{bb'}(Q^2,\mu_F^2,\mu_R^2)

where the sum runs over all contributing partons :math:`p\in\{g,q,\bar q\}`. In the following we will
assume that a quark :math:`\hat q` is hit by the boson. Note that this is *independent* of the incoming
parton :math:`p`.

Using |pQCD| we expand the partonic structure functions in powers of the strong coupling
:math:`a_s(\mu_R^2) = \frac{\alpha_s(\mu_R^2)}{4\pi}`:

.. math ::
    \mathcal F_{k,p}^{bb'}(z, Q^2,\mu_F^2,\mu_R^2) = \sum_{l=0} a_s^l(\mu_R^2) \mathcal F_{k,p}^{bb',(l)}(z, Q^2,\mu_F^2,\mu_R^2)

Note that these two equations have to be checked for every reference as lots of different
normalization are used in practice.

Similar to the splitting on the leptonic side we have to split on the partonic side again:

.. math ::
    \mathcal F_{k,p}^{bb'} &= g_{\hat q,b}^V g_{\hat q,b'}^V \mathcal F_{k,p}^{VV} + g_{\hat q,b}^A g_{\hat q,b'}^A \mathcal F_{k,p}^{AA}~,~ k\in\{1,2,L\} \\
    \mathcal F_{3,p}^{bb'} &= g_{\hat q,b}^V g_{\hat q,b'}^A \mathcal F_{3,p}^{VA}

Implementation: :meth:`~yadism.coupling_constants.CouplingConstants.partonic_coupling`

The dependence on the factorization scale :math:`\mu_F^2` and renormalization scale :math:`\mu_R^2`
is discussed :doc:`here </theory/scale-variations>`.
