Benchmark Runner
================

.. todo::

   It is not anymore an ecosystem of scripts but a proper object-oriented
   python subpackage.

   - update the status
   - describe the description of the API (how the user can interact with the
     runner itself)
   - describe the current design

DBinterface
-----------

External Utils
--------------

APFEL Utils
~~~~~~~~~~~
- python bindings is provided natively by the project
- a loader is provided internally, that allows the user to obtain a running
  ``apfel`` just providing a dictionary (it is based on the analogous one
  provided by the project itself in the C++ wrapper)
- a runner is provided internally, plugging a caching system for speeding up
  the benchmarks (since APFEL is a stable code, that we are not developing, a
  given input will yield deterministically one and only one output)

QCDNUM Utils
~~~~~~~~~~~~
- python bindings are provided by us externally
- the QCDNUM runner is provided internally, based on the bindings
- a runner is provided internally, based on the bindings; it plugs a caching
  system for speeding up the benchmarks (since QCDNUM is a stable code, that we
  are not developing, a given input will yield deterministically one and only
  one output)
