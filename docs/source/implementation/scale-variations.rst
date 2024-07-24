.. _implement-sv:

Scale Variations
================

The scale variations are universal, since they depend only on the incoming
structure (they are related to the input partons), so they act multiplicatively
on the process itself (in particular through convolution), see the :ref:`theory
section <theory-sv>`.

Then it is worth to exploit this property as much as possible to simplify the
implementation and maintainability of the code.

Numerical convolutions
----------------------

The two alternatives for the convolutions are the following:

1. doing it analytically, and code all the expressions
2. code only the basic elements and use them in numerical convolutions

The strategy chosen by ``yadism`` is partially (more later on, see `Multiple
convolutions`_) the second, because essentially of a couple of advantages:

- the expressions have to be coded only once, instead of doing it for each
  coefficient function (perturbative order, structure function, partonic
  channel, and heavyness)
- the coefficient function expressions, and the splitting functions too, become
  rapidly more and more cumbersome while increasing the perturbative order, in
  this way it is possible to save many complicate convolutions

The main disadvantages would be the following:

- doing convolutions numerically **precision** is lost
- numerical integrations are **time-consuming**

Actually this two issues have a negligible impact on the result, indeed the
numerical precision is absolutely **dominated by the interpolation** required to
integrate a generic PDF set (and in general PDF sets are delivered as
interpolation grids, so they are never exact functions) and since the
contributions are universal they can be **computed just once** per interpolation
grid (and so actually once per run) and simply applied at the cost of a matrix
product.

Moreover integrating analytical expressions (such as the convolution
of splitting functions and coefficient functions, that is more complicated than
both) is difficult and so: it can deteriorate the precision of the integration
and require more evaluations, and so it is also time-consuming.

Baseline: it is not clear that the disadvantages would be improved at all by the
other choice, but the advantage is instead clear and great.

Multiple convolutions
~~~~~~~~~~~~~~~~~~~~~

Actually there are multiple convolutions involved, see the :ref:`factorization
scale variation formula <theory/scale-variations:Factorization>`.

What is done in ``yadism`` is to implement everything to depend only on the
*original* coefficients :math:`\textbf{c}_a^{(i)}`, and not to depend recursively
on the convolved ones :math:`\textbf{c}_a^{(i,j)}`, in order to limit the number
of extra numerical convolutions to a single one.

In this case we are avoiding the disadvantages of the previous section, only
partially paying for giving up on of the advantages: these convolutions would
involve only splitting functions, and never the coefficient functions'
expressions, and for this same reason they are also considerably easier.

Applying convolved kernels
---------------------------

Since the convolutions are done numerically it is needed to integrate ahead of
time the full operator: indeed the splitting functions act as operator on
coefficient functions, taking them as input and providing other coefficients as
output (through convolutions), exactly like an `EKO`_.

.. _EKO: https://eko.readthedocs.io/en/latest/theory/DGLAP.html

Indeed factorization scale variations are simply encoding bits of evolution
directly inside the coefficient functions.

Actually coefficient functions have their own representation in ``yadism`` as
:ref:`kernels <implementation/kernels:Kernels>`, i.e. a pair of a coefficient
function and some weights, possibly related to multiple partonic channels.

The weights usually encodes charge factors, that is the only part that
differs in the contributions of different flavors, related to single set of
diagrams.

The splitting functions are also non-trivial in flavor space, but the only
non-triviality manifest in the `anomalous dimension basis
<https://eko.readthedocs.io/en/latest/theory/FlavorSpace.html#operator-anomalous-dimension-basis>`_,
that is a very restricted basis (dimension 7) for the operators on the flavor
space (whose dimension is :math:`13 \times 13`, with the contributions of 12
quark flavors and the gluon).

Because of this we can apply splitting functions (and their convolutions) in two
objects: the :math:`x`-space expression, and the projector relative to the space
it acts on.

.. important::

   The final formula related to the application of scale variations is the
   following:

   .. math::

      c_{a, (\beta, j)}^{(out, lnf)} = v_\alpha \Pi^{(ad)}_{\alpha\beta} S^{(ad), (out, lnf, in)}_{ji} c^{(in)}_{a,i}

   where:

   - :math:`v` are the weights assigned to each partonic channel
   - :math:`\Pi` are the projectors over the subspaces related to the anomalous
     dimension basis
   - :math:`S` are the splitting kernels
   - :math:`c` are the actual raw (non-scale-varied) coefficient functions on
     the right hand side, and the dressed (scale-varied) ones on the left

   and so:

   1. :math:`(out, lnf, in)` are respectively indexing: the perturbative order of
      the generated coefficient, the power of :math:`\log(Q^2/\mu_F)` the generated
      coefficient is multiplied by, and the perturbative order of the coefficient
      is applied on
   2. :math:`(ad)` is an index over the anomalous dimension basis
   3. :math:`\alpha, \beta` are indices in flavor space
   4. :math:`i, j` are indices in the evolution space
   5. :math:`a` is the structure function kind


Notice that the part that involves the flavor space is only coupled to the part
that involves the interpolation space by the sum over the anomalous dimension
basis, that is relatively small (dimension 7), so the two sums are done
separately and only recombined at the latest possible moment.

Integrating in x-space
~~~~~~~~~~~~~~~~~~~~~~

The factorization theorem can be schematically written for scale variations as:

.. math::

   F = f \otimes S \otimes c

Where :math:`F` is the observable, :math:`f` the |PDF|, :math:`c` the raw
coefficient function, and :math:`S` the splitting kernels organized as described
in the theory section.

Without the scale variations the interpolation is done completely on the |PDF|,
as described in :doc:`interpolation`, and the interpolation polynomials would
then be used to convolve numerically the coefficient functions:

.. math::

   F(x) &= [f \otimes c] (x) =  \left[\left(\sum_j f(x_j) p_j\right) \otimes c\right](x) =\\
   &= \sum_j f(x_j) \left[p_j \otimes c\right](x) = \sum_j f(x_j) c_j(x)

In this way for each kinematic specified :math:`x` the coefficient function is
turned into a vector over interpolation basis.
And so:

.. math::

   c_j(x) = (p_j \otimes c) (x)

The same thing can be done with scale variations, turning the :math:`S` kernels
into a matrix.

.. math::

   F(x) &= [f \otimes c] (x) =  \left[\left(\sum_j f(x_j) p_j\right) \otimes S \otimes c\right](x) =\\
   &= \sum_j f(x_j) \left[p_j \otimes S \otimes c\right](x)\\
   &= \sum_j f(x_j) \left[\left(\sum_k (p_j \otimes S)(x_k) p_k\right) \otimes c\right](x)\\
   &= \sum_{jk} f(x_j) \left[(p_j \otimes S)(x_k)\, (p_k \otimes c)\right](x)\\
   &= \sum_{jk} f(x_j)\, S_{jk}\, c_k(x)

Where essentially the |PDF| have been interpolated first, and then the
convolution of the interpolation basis and the splitting kernel (:math:`p_j
\otimes S`) is also interpolated a second time.

.. important::

   Note that:

   .. math::

      S_{jk} = (p_j \otimes S)(x_k)

   So even if the two indices run **on the same basis**, they have actually
   **different sources**:

   1. the first one, :math:`j`, is coming from the convolution with the
      interpolation polynomial :math:`p_j` (same as for the coefficient function
      :math:`c_j(x)`, because actually :math:`S \otimes c` is the scale-varied
      coefficient function)
   2. the second, :math:`k`, is coming from the evaluation on the grid point
      :math:`x_k` (to be joined with the coefficient function `c_k(x)`, who is
      stemming from)


Remark on projectors
~~~~~~~~~~~~~~~~~~~~

The projectors are not very complicate objects, but a little bit of care has to
be used relatively to their normalization.

Indeed the actual expression for the diagonal projectors is the following:

.. math::

   \Pi^{(a)} = \sum_{k \in a} \frac{\dyad{k}{k}}{\abs{\bra{k}\ket{k}}^2}

where the projectors over single states are explicitly normalized with the norm
of the state, since the evolution basis itself is not normalized.

.. note::

   The sum is present because some anomalous dimension basis element do apply to
   more than a single evolution flavor, referring actual to a subspace rather
   than a single vector.

   e.g.: for :math:`a = ns_+` the distributions involved are

   .. math::

      T_3, T_8, T_{15}, T_{24}, T_{35}

   cut if there are less than 6 active flavors. For the full correspondence see
   the `related eko's documentation
   <https://eko.readthedocs.io/en/latest/theory/FlavorSpace.html#operator-anomalous-dimension-basis>`_.

But in order to explicit the prescription for the off-diagonal elements the
following has to be noticed:

- the projector are made of a :math:`\bra{in}` that has to be contracted with the
  incoming |PDF|, for this reason this has to remain unnormalized, in order to
  obtain the required contributions for the unnormalized evolution basis (i.e.
  it has to be the same contribution that would have been if directly applied to
  the raw coefficient function)
- the other component is a :math:`\ket{out}` that goes together the
  non-scale-varied coefficient function itself, thus it has to be normalized,
  because it should extract


E.g.: if the singlet |PDF| is plugged in, written in flavor basis, when no scale
variations are present it would apply directly to the coefficient function,
without any extra normalization

.. math::

   \bra{c_\Sigma}\ket{\Sigma}

and the same should happen in case of scale variations: if the singlet is going
to split a gluon then the singlet PDF has to contribute with the gluon
coefficient function, so the last has to become singlet proportional:

.. math::

   \bra{c_g}\dyad{g}{\Sigma} \times \ket{\Sigma}

while in the case of quark contributions to the gluon channel it has to be
normalized.

*Another, more practical, point of view is that this is because* :math:`P_{ab}`
*already contains the normalization, e.g.* :math:`P_{qg} \propto 2 n_f` *, and
thus it has to be subtracted from there in order to use the unnormalized
projector).*

.. important::
   The actual expression for all projectors is then the following:

   .. math::

      \Pi^{(a)} = \sum_{(o, i) \in a} \frac{\dyad{o}{i}}{\abs{\bra{o}\ket{o}}^2}



Renormalization scale variations
--------------------------------

The renormalization scale variations up to |NLO| consist only in the evaluation
of the strong coupling :math:`\alpha_s` at a different scale.

Instead, starting at |NNLO|, there are further contributions to the coefficient
functions anomalous to those discussed in the previous paragraph.

These contributions do not require convolutions, they are reported in the
:ref:`theory section <theory/scale-variations:Renormalization>`, and in
``yadism`` they are actually implemented as they are written, i.e.:

- first compute the factorization scale variations, and derive
  :math:`\textbf{C}_a^{(i)}(x, L_M, 0)` from the :math:`\textbf{c}_a^{(l)}(x)`
- then apply the further corrections on top of the new object, and obtain the
  full :math:`\textbf{C}_a^{(i)}(x, L_M, L_R)`

.. attention::

   The parameter :math:`L_R = \log(\mu_F^2 / \mu_R^2)`, so it does not account
   for the difference between the process scale :math:`Q^2` and the
   renormalization one :math:`\mu_R^2`, but between the latter and the
   factorization one :math:`\mu_F^2`.

   For the user convenience the result is nevertheless stored in grids in which
   the parameters are instead:

   - :math:`\log(\mu_F^2 / Q^2)`
   - :math:`\log(\mu_R^2 / Q^2)`
