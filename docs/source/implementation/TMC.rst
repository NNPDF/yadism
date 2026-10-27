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
effects relating to the non-zero mass of the target. In particular, 
this has an effect in the large-x region. 
In the Björken limit, where 
:math:`Q^2 >> M^2,` we can in principle neglect terms proportional to the
expansion parameter :math:`M^2/Q^2`. 
For a nucleon of finite mass and at low :math:`Q^2`, however, this expansion 
parameter grows and becomes non-negligible. Target-mass corrections account
for these effects, which arise from the trace of the twist-2 operators in the OPE.
Since the TMCs are not dependent on the perturbative order, they are a kinematic correction that applies to every order.

Kinematics
----------

In practice, TMCs amount to a shift in kinematics and a reweighting.
We define the Nachtmann variable, with which we rescale :math:`x`:
:math:`\xi_N = \frac{2x}{1+r},`
with 
:math:`r = \sqrt{1+\frac{4x^2M^2}{Q^2}}.`
One notices that in the case where :math:`M\rightarrow 0`, :math:`\xi_N \rightarrow x`, 
and the TMCs disappear.

The structure functions can therefore be expressed in terms of the bare (noTMC) structure functions,
evaluated at the rescaled Nachtmann variable, for example in the case of :math:`F_2` as follows:

:math:`F_2^{\mathrm{TMC}}(x,Q^2) = \frac{x^2}{\xi^2_Nr^3}F_2^{\mathrm{noTMC}}(\xi_N,Q^2) + \frac{6M^2x^3}{Q^2r^4}h_2(\xi_N,Q^2) + \frac{12M^4x^4}{Q^4r^5}g_2(\xi_N,Q^2)`

with

:math:`h_2(\xi_N,Q^2) = \left(\frac{z}{\xi_N} \otimes F_2^{\mathrm{noTMC}}(Q^2)\right)(\xi_N)`
:math:`g_2(\xi_N,Q^2) = \left((1-z) \otimes F_2^{\mathrm{noTMC}}(Q^2)\right)(\xi_N).`
Similar equations exist for :math:`F_1`, :math:`F_L`, and :math:`F_3`, all of which have been 
implemented in YADISM.
One notices that the equations above are convolutions, so a simple pointwise evaluation has been turned
into a convolution. Given that we precompute the structure functions on an interpolation grid,
these more complex objects need to befolded into the precomputed objects, increasing the size of the output
and slowing down the calculation. YADISM therefore implemented an approximation that reduces things back
to a simple evaluation,
:math:`F_2^{\mathrm{TMC}}(x,Q^2) \approx \frac{x^2}{\xi^2_Nr^3}F_2^{\mathrm{noTMC}}(\xi_N,Q^2)\left(1+\frac{6M^2x\xi_N}{Q^2r}(1-\xi_N)\right)`

In YADISM
---------

One can enable TMCs with the ``TMC`` flag in the input runcard, with multiple options:
- **TMC: 0 (Disabled)**:
  No target mass corrections are applied and the SFs are evaluated at :math:`(x,Q^2)`.
- **TMC: 1 (APFEL)**
  The ``APFEL`` formalism is used, including twist-4 :ref:`nnpdf-1.0`.
- **TMC: 2 (Approx)**
  The approximation mentioned above is used to speed up the calculation.
- **TMC: 3 (Exact)**
  The full expression is used, including twist-6.

Implemenation
-------------

Similar to how the TMC corrected structure functions are defined on top of the bare ones, the
structures in the code form an intermediate block between the class :class:`~yadism.esf.StructureFunction`
and the actual calculator :class:`~yadism.esf.EvaluatedStructureFunction` - in a sense they are the replacement for the latter.

The :class:`~yadism.runner` class contains the main loop for calculation and holds a list of structure function instances, 
that will manage the calculation.
:class:`~yadism.esf.StructureFunction` is the manager. It holds a reference to its parent runner, 
such that it is also able to access its :class:`~yadism.esf.StructureFunction` siblings. It instantiates
:class:`~yadism.esf.tmc.EvaluatedStructureFunctionTMC` according to the ``TMC`` flag, as opposed to
its TMC-less sibling :class:`~yadism.esf.tmc.EvaluatedStructureFunctionTMC`.

Caching
-------
Caching is managed at the level of :class:`~yadism.esf.StructureFunction` (SF), while the values are
kept at the level of ``ESF``, so the SF is just routing the caller to the correct instance of
``ESF`` to ask for values. The layout is the following:

- The SF instantiates an ``ESF`` or an ``ESFTMC`` according to the ``TMC`` flag in the theory
  dictionary, and appends it to ``self.esfs`` at load time, i.e. in ``self.load()`` (these are the
  observables to be computed).
- When asked for output without TMC, an ``ESF`` is called and the instance is registered:

    - ``self.get_output()`` is used for getting the result, passing through.
    - ``self.get_ESF()`` which is used for getting the instance and registering it in the cache.

- With TMC turned on, an ``ESFTMC`` is called, and whenever it needs an ``ESF`` instance to compute a point
  it asks its parent SF through the ``SF.get_ESF()`` method, in this way also passing through the
  cache.


References
----------
See also :ref:`felix-revisited` for a more detailed explanation.
