Code Structure
==============

In this section the structure of the package is discussed in details, from the
point of view of the implementation of course, but mainly concerning the
overall project and the organization of the many ingredients/features composing
this package.

A brief outline can instead be found in the :doc:`introductive page
<../yadism>`.

.. toctree::
   :maxdepth: 2

   runner
   SF
   ESF
   TMC


Brief Descriptions
------------------
First of all let's introduce a little bit more the `yadism` hierarchy.

`yadism`'s class hierarchy actually spans two dimensions:

- **height:** starting from the main :py:class:`Runner` there is a stack of
  interfaces and server classes;

  the implementation of this dimension is through **ownership** of an object on
  a set of objects of the level directly below;
  an outline of the so:

  - :py:class:`Runner`, see `Runner`_ below
  - :py:class:`StructureFunction`, see `Structure Function`_ below
  - :py:class:`EvaluatedStructureFunction` 


- **depth:** all the objects develop an internal hierarchy, used to factorize
  all the common features and to delegate only the defining differences to the
  lowest nodes;

  the implementation of this dimension is through **inheritance**, so from the
  point of view of the previous dimension all the elements of a single node
  look really the same, implementing the very same interface;

  most often the base classes in this hierarchy are abstract classes
  (subclasses of :py:class:`abc.ABC` with some methods decorated with
  :py:func:`abc.abstractmethod`), so they are not instantiable themselves, even
  if they implement most of the logic (but the missing pieces are necessary to
  have a working instance);

  an example of this is the :py:class:`EvaluatedStructureFunction` internal
  hierarchy, see `ESF hierarchy`_ below


Runner
~~~~~~
This is the main interface, managing the full computation process, and it is
the only object the final user should interact with, providing proper input and
getting from the desired output

Structure Function
~~~~~~~~~~~~~~~~~~
This is an internal interface, that manage the computation internally to each
observable kind, and return the result of the calculation to its owner through
proper methods; each of these object will in general manage the calculation of
multiple atomic instances


Evaluated Structure Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This structure is the lowest one in the height hierarchy.

This class and its siblings (like :py:class:`EvaluatedStructureFunctionTMC`)
are the atomic object, responsible for the calculation of a single observables
(i.e. a fully specified physical observable on a single fully specified
kinematic point, e.g. F2light(x, Q2))

ESF hierarchy
"""""""""""""
The `ESF` internal hierarchy, bulding an inheritance chain

- :py:class:`EvaluatedStructureFunction` is the base class, and specify the
  constructor, the output method and even the full calculation process, but
  it still misses the physics, that it is not specified at this level
- classes :py:class:`EvaluatedStructureFunctionLight` and
  :py:class:`EvaluatedStructureFunctionHeavy` factorize all the differences
  related to the treatment of structure functions with DIS boson coupling to
  either a light or a heavy quark flavour
- classes :py:class:`EvaluatedStructureFunctionF2light`,
  :py:class:`EvaluatedStructureFunctionF2charm`,
  :py:class:`EvaluatedStructureFunctionF2bottom`,
  :py:class:`EvaluatedStructureFunctionF2top`,
  :py:class:`EvaluatedStructureFunctionFLlight`, ... are the final classes,
  inheriting all the structures from above and only responsible to define the
  mathematical expressions of the related coefficient functions
