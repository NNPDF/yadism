Code Structure
==============

In this section the structure of the package is discussed in details, from the
point of view of the implementation of course, but mainly concerning the
overall project and the organization of the many ingredients/features composing
this package.


Brief Description
-----------------

`yadism` is organized in two different parts:

- the **physics-related** part, that includes a storage of coefficient functions
  expressions (`PartonicChannel`), the coupling constants (charges) related to the |EW| boson
  coupling (`CouplingConstants`), and the suitable joining between the two (`Kernel`)

  all these elements are contained inside the `coefficient_function` subpackage,
  and they are provided to the outside through `Combiner`, that recollects all
  the `Kernel` relevant for a given calculation

- the **computational** part, that is fully managed by a `Runner` instance, and
  is composed of different elements, used for applying all the relevant steps
  for the requested calculation

Essentially the flow of an execution is the following:

1. (**user** initiated) a :class:`~yadism.runner.Runner` is instantiated and it
   is passed the theory configuration, and the requested observables to compute
   (together with related configurations)
2. a check is performed on the user input (by an
   :class:`~yadism.input.inspector.Inspector`)
3. the relevant global *service providers* are initialized and stored by the
   :class:`~yadism.runner.Runner` (like the :math:`\alpha_s` evolution, or the
   interpolation dispatcher, or the couplings computer)
4. the requested observables are scanned, and they are assigned to the
   respective :class:`~yadism.sf.StructureFunction` /
   :class:`~yadism.xs.CrossSection` (acting as manager and caching storage)
   according to their kind and heavyness (but multiple kinematics will belong to
   the same :class:`~yadism.sf.StructureFunction` /
   :class:`~yadism.xs.CrossSection`) each kinematic point will correspond to an instance of
   :class:`~yadism.esf.esf.EvaluatedStructureFunction` / :class:`~yadism.esf.exs.EvaluatedCrossSection`

5. (**user** initiated) output is requested
6. the request is propagated to the managers, and then to all the required
   `ESF` objects
7. the `ESF` issues a request to the
   :class:`~yadism.coefficient_functions.Combiner` for the relevant
   :class:`~yadism.coefficient_functions.kernels.Kernel`
8. all the :class:`~yadism.coefficient_functions.kernels.Kernel` are numerically
   convoluted with the |PDF| interpolation polynomials
9. all the results are collected in an :class:`~yadism.output.Output` object and
   returned to the user
10. (**user** initiated) the :class:`~yadism.output.Output` object might be
    dumped on disk in one of the available formats

Elements
--------

.. toctree::
   :maxdepth: 2

   runner
   input
   kernels
   SF
   ESF
   interpolation
