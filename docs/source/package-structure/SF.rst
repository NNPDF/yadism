Structure Function interface
============================

A `StructureFunction` object is actually a structure functions manager, and an
interface between the :doc:`Runner <runner>` instance and the actual
|SF| calculator, i.e. :doc:`EvaluatedStructureFunction
<ESF>` instances.

On the opposite of |ESF| case there is a single kind `StructureFunction`,
nevertheless each instance should be considered of a given kind, e.g. `F2light`
or `FLbottom`, and this information is stored as the attribute `name` of the
instance.

Lifecycle
---------
1. A |SF| object should be instantiated passing all those information needed to
   perform calculation (see next `Handling parameters`_).
2. Then it is loaded with kinematic points to be computed, using its `load`
   method, and they are used (converted in some sense) into a list of |ESF|
   instances, mapped one to one on the requested kinematic configurations.
3. Eventually you can request to perform the calculations for all the loaded
   observables just asking for the output, through the `get_result` method

Handling parameters
-------------------
There are four categories of parameters passed to a |SF| when instantiated:

1. its name, that identify its kind (e.g. `F2light` or `F2bottom`)
2. a reference to the `Runner` instance that owns it, used in task routing in
   the caching protocol, to retrieve the other |SF| objects owned by the same
   `Runner` (see `Caching`_)
3. external handlers, in charge of specific tasks (like computing the
   :math:`\alpha_s` value, or manage the interpolation business)
4. theory parameters

All these parameters are stored **at this level** and not passed down to any
|ESF| -like object.
So anything needed for the calculation, such as the external handlers, or
theory parameters, is always retrieved by a |ESF| object asking to its |SF|
parent (so the |ESF| will keep a reference of it).

Caching
-------
The caching system goal is to keep the result of already computed |ESF| to
reuse them if needed in multiple calculations during the lifecycle of a single
:doc:`Runner <runner>` instance.

Cache is implemented on two levels:

- a global management system, implemented in a distributed way across the |SF|
  instances, such that each |SF| object is responsible:
  
  1. for the caching of the |ESF| corresponding to its kind
  2. to redirect the requests for different kind of |ESF| coming from any of
     the managed |ESF| (i.e. one of those it is responsible to cache)

- a local caching mechanism, implemented at the level of the single |ESF|
  object, that stores its result as soon as it calculates it the first time,
  and never recomputes (further details at :doc:`ESF <ESF>`)


