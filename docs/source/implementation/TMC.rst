Target Mass Corrections
=======================

The master equation for DIS,
:math:`\sigma(x,Q^2) = \Sum_j\int_x^1 \frac{dz}{z}C_j(z,Q^2)f_j(\xi=x/z,Q^2)+\mathcal{O}\left(\frac{\Lambda^2_{\mathrm{QCD}}}{Q^2}\right)`
can be evaluated in pertubative QCD (pQCD) in the collinear factorization scheme. 

However, we observe that there are non-perturbative corrections,
which elicits the concept of leading and higher twist. These higher twist contributions are summarized as
:math:`\mathcal{O}\left(\frac{\Lambda^2_{\mathrm{QCD}}}{Q^2}\right)`.
An important distinction to make, is that PDFs are well-defined, renormalized, 
gauge-invariant, and non-perturbative quantities. The notion that they are 
leading-twist objects only comes in where they enter the power expansion of a hard-scattering observable.


These corrections :math:`\mathcal{O}\left(\frac{\Lambda^2_{\mathrm{QCD}}}{Q^2}\right)` are complex and
contain many non-perturbative matrix elements and depend on multiparton correlations. Indeed,
properly separating the leading-twist terms from higher-twist terms correlations is difficult and
unstable.

A part of these higher-twist terms however, so called target mass corrections (TMCs), are
calculable systematically and consistently. These are required in order to correct for 
effects relating to the non-zero mass of the target. Target-mass corrections account
for these effects, which arise from the trace of the twist-2 operators in the OPE.
Since the TMCs are not dependent on the perturbative order, they are a kinematic correction that applies to every order.
In particular, this has an effect in the large-:math:`x`, small-:math:`Q^2` region. 

The :math:`W^2` cut
-------------------
In DIS, among :doc:`../theory/intro <other kinematic quantities>`, we can define
:math:`W^2 = (P+q)^2 = M^2 + 2P\dot q + q^2`
with
:math:`Q^2 = -q^2, \, \, \, \, x = \frac{Q^2}{2P \dot q},`
so that
:math:`W^2 = M^2 + Q^2\left( \frac{1}{x} - 1\right).`
This quantity :math:`W^2` is defined as the invariant mass squared of the hadronic system,
produced when a virtual boson interacts with the targeted nucleon.
It is just as important as :math:`Q^2` in DIS: :math:`Q^2` sets the scale of the interaction,
and :math:`W^2` sets the energy available to the final state. At fixed :math:`Q^2`,
large :math:`x` means small :math:`W^2` and vice versa, so the high-:math:`x` region
is exactly where the final state is low-mass and TMCs gain in effect.

A scattering is inelastic when the nucleon breaks up, i.e. when :math:`W^2 > M^2`. 
On the other hand, in the elastic limit of :math:`x=1`, the nucleon stays fully intact,
and the scattering is elastic. For the proton, :math:`M \simeq 0.938` GeV, so
:math:`W^2 \simeq 1.5 \mathrm{GeV}^2`. A process only counts as deep-inelastic when
:math:`Q^2` is large enough for pQCD to apply, and :math:`W^2` is large enough
to be above the resonance region.
In the Björken limit, where 
:math:`Q^2 >> M^2,` we can in principle neglect terms proportional to the
expansion parameter :math:`M^2/Q^2`. 
For a nucleon of finite mass and at low :math:`Q^2`, however, this expansion 
parameter grows and becomes non-negligible, so TMCs become non-negligible. 
Therefore, :math:`W^2` is an effective measure to define the region in which TMCs,
among other resonance effects, become large. Placing a cut on :math:`W^2`
restricts the accesible :math:`x` range at a given :math:`Q^2` and allows us to exclude
the region in which TMCs become important. 
In ``NNPDF`` fits, typical values are :math:`W^2_{\mathrm{cut}} > 12.5 \mathrm{GeV}^2` and
:math:`Q^2_{\mathrm{cut}} > 3.49 \mathrm{GeV}^2` to err on the safe side: TMCs are included,
and cuts are placed to ensure the scattering is deep-inelastic and we are above the resonance limit.

Kinematics
----------

In practice, TMCs amount to a shift in kinematics and a reweighting.
We define the Nachtmann variable, with which we rescale :math:`x`:
:math:`\xi_N = \frac{2x}{1+r},`
with 
:math:`r = \sqrt{1+\frac{4x^2M^2}{Q^2}}.`
One notices that in the case where :math:`M\rightarrow 0` and :math:`\xi_N \rightarrow x`, 
the TMCs disappear.

The structure functions can therefore be expressed in terms of the bare (noTMC) structure functions,
evaluated at the rescaled Nachtmann variable, for example in the case of :math:`F_2` as follows :cite:`blub`:

:math:`F_2^{\mathrm{TMC}}(x,Q^2) = \frac{x^2}{\xi^2_Nr^3}F_2^{\mathrm{noTMC}}(\xi_N,Q^2) + \frac{6M^2x^3}{Q^2r^4}h_2(\xi_N,Q^2) + \frac{12M^4x^4}{Q^4r^5}g_2(\xi_N,Q^2)`

with

:math:`h_2(\xi_N,Q^2) = \left(\frac{z}{\xi_N} \otimes F_2^{\mathrm{noTMC}}(Q^2)\right)(\xi_N)`
:math:`g_2(\xi_N,Q^2) = \left((1-z) \otimes F_2^{\mathrm{noTMC}}(Q^2)\right)(\xi_N).`
Similar equations exist for :math:`F_1`, :math:`F_L`, and :math:`F_3`, all of which have been 
implemented in YADISM.
One notices that the equations above are convolutions, so a simple pointwise evaluation has been turned
into a convolution. Given that we precompute the structure functions on an interpolation grid,
these more complex objects need to be folded into the precomputed objects, increasing the size of the output
and slowing down the calculation. YADISM therefore implemented an approximation that reduces things back
to a simple evaluation,
:math:`F_2^{\mathrm{TMC}}(x,Q^2) \approx \frac{x^2}{\xi^2_Nr^3}F_2^{\mathrm{noTMC}}(\xi_N,Q^2)\left(1+\frac{6M^2x\xi_N}{Q^2r}(1-\xi_N)\right)`

In YADISM
---------

One can enable TMCs with the ``TMC`` flag in the input runcard, with multiple options:

- **TMC: 0 (Disabled)**:
  No target mass corrections are applied and the SFs are evaluated at :math:`(x,Q^2)`.
- **TMC: 1 (APFEL)**:
  The ``APFEL`` formalism is used (see :ref:`nnpdf-1.0`). This is the expression
  above with the :math:`g_2` term dropped, i.e. only the shifted
  structure function and the :math:`h_2` convolution are kept.
- **TMC: 2 (Approx)**:
  The approximation mentioned above is used to speed up the calculation. The
  convolutions are replaced by a simple evaluation of the bare structure
  function at :math:`\xi_N`, so no convolution is required.
- **TMC: 3 (Exact)**:
  The full expression above is used, including both the :math:`h_2` and the
  :math:`g_2` convolutions.

Implementation
--------------

Similar to how the TMC corrected structure functions are defined on top of the bare ones, the
structures in the code form an intermediate block between the class :class:`~yadism.esf.StructureFunction`
and the actual calculator :class:`~yadism.esf.EvaluatedStructureFunction` - in a sense they are the replacement for the latter.

:class:`~yadism.esf.StructureFunction` is the manager. It holds a reference to its parent runner, 
such that it is also able to access its :class:`~yadism.esf.StructureFunction` siblings (``FL_TMC`` also 
requires terms built from the bare ``F2``. It instantiates
:class:`~yadism.esf.tmc.EvaluatedStructureFunctionTMC` according to the ``TMC`` flag, as opposed to
its TMC-less sibling :class:`~yadism.esf.tmc.EvaluatedStructureFunction`.

Caching
-------
A TMC-corrected structure function is built from bare structure functions at other points. Computing
a bare strucure function is expensive, and the same bare value is often needed many times:

- :math:`F_2^{\mathrm{TMC}}(x, Q2)` needs the bare :math:`F2` at the shifted point :math:`(\xi_N, Q^2)`.
- In the APFEL and exact modes, it also needs the convolutions :math:`h_2` and
  :math:`g_2`. These need the bare :math:`F2` at each interpolation-grid point
  :math:`x_j` (at the same :math:`Q^2`).
- Different requested points with the same :math:`Q^2` need the same grid points.
  Also, :math:`F_L^{\mathrm{TMC}}` needs the bare :math:`F_2` in addition to the bare :math:`F_L`.

We need to cache these values, because each of these quantities would be recomputed every time,
which is redundant because we know they use the same (global) interpolation points.

Caching is managed at the level of :class:`~yadism.esf.StructureFunction` (``SF``), while the values are
kept at the level of ``ESF``, so the ``SF`` is just routing the caller to the correct instance of
``ESF`` to ask for values:

- The ``SF`` instantiates an ``ESFTMC``, and for each one it calls ``SF.get_ESF(kind, kinematics)`` on its parent ``SF``.
  It appends this to ``self.esfs`` at load time, i.e. in ``self.load()`` (these are the observables to be computed).
  For ``F_L`` or ``F_3`` corrections it can ask for a different kind, which it reaches through the parent ``runner``.
- The ``SF`` checks whether an ``ESF`` already exists. If yes, it returns it without recomputing, and if no, it is
  created, registered in the cache, and returned.

References
----------
:cite:`Schienbein:2007gr`
