.. DIS documentation master file.


#################
DIS documentation
#################

.. the following transition is only used for highlight the main title

---------

`yadism` is a wonderful package for computing |DIS| observables replacing the
corresponding one inside |APFEL|.

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   yadism.rst
   dev.rst
   interpolation.rst

   zzz-refs.rst

In these :underlined:`documents` you can find the reference for all *yadism* API and internals.


Features
~~~~~~~~
Current features:

- |LO| structure functions (|NC|)
- |NLO| structure functions (|NC|)
- |NLO| scale variations


.. toctree::
   :maxdepth: 1
   :caption: Theory

   theory/LO.rst
   theory/NLO.rst
   theory/NNLO.rst
   theory/N3LO.rst
   theory/heavy-flavors.rst
   theory/scale-variations.rst
   theory/TMC.rst

And here there is some *physics documentation*.

Some of these are trivial and will be replaced, they are here just to create a
structure.


Dev Tools
~~~~~~~~~
Current tools:

- benchmark db suite
  - db generating scripts
  - navigator
- benchmark runner
  - currently in `benchmarks/conftest.py`
- actual tests/benchmarks
  - unit tests
  - regression tests
  - benchmark (against APFEL)
- third-party tools

.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   dev-tools/db-suite.rst
   dev-tools/benchmark-runner.rst
   dev-tools/tests.rst
   dev-tools/third-party.rst

And here there is some *physics documentation*.

Some of these are trivial and will be replaced, they are here just to create a
structure.

---------


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
