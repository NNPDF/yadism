Evaluated Structure Function
============================

The :class:`EvaluatedStructureFunction` is the actual calculator of the
coefficient functions, indeed it is not possible to perform the calculation
until the kinematics has not been fully specified.

Each one of this object is created for a single kinematic point, and
initialized with it at construction time.

No object is recycled for more than a single calculation, and it's not deleted
before the destruction of its ancestor :class:`Runner` instance.
For this reason once that its result has been computed the object is kept and
used as the atomic part of the caching system.

Kinds
~~~~~
There are more kinds of :class:`EvaluatedStructureFunction`, and each instance
belong to a :class:`StructureFunction` instance of the respective kind.

The kinds are defined by choosing one option for each of the following classes:

- ``F2``, ``FL``, ``F3``, ``g1``, `gL``, `g4``
- ``light``, ``charm``, ``bottom``, ``top``, or ``total``

Sometimes an instance of a different kind it is needed to complete the
calculation, for one of the following reasons:

1. it is not always possible to determine the exact kind involved in the
   calculation before having the final kinematics is available;

   *for example*: if ``F2charm`` is requested but the Flavor Number Scheme is
   `FFNS4` than the calculation should be performed as it were a light and not
   an heavy quark, but the information about how to compute the light
   contributions is hold by ``F2light`` and not duplicated
2. the observable definition depends on other observables;

   *for example*: ``F*total`` is defined as the sum of ``F*light``,
   ``F*charm``, ``F*bottom`` and ``F*top``

In these cases the instance will determine which one is the kind (or kinds)
required to complete the calculation, and it will ask its direct ancestor
(the unique :class:`StructureFunction` instance of that :class:`Runner` of the
correct kind) for the instance needed.

Once the instance has been obtained it is asked for its result.

ESFResult
---------

.. todo::

   Write a brief description of the ESFResult's attributes and methods.
