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
   tutorials/index.rst
   interpolation.rst

   zzz-refs.rst

In these :underlined:`documents` you can find the reference for all *yadism* API and internals.


Features
~~~~~~~~
Current features:

- |LO| structure functions (|EM|)
- |NLO| structure functions (|EM|)
- |NLO| scale variations


.. toctree::
   :maxdepth: 1
   :caption: Theory

   theory/DIS-intro.rst
   theory/coeff-funcs.rst 
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

This tools have been developed alongside `yadism`, in order to automatize tests
and improve the quality of code (less bugs, more readable... hopefully...).

---------


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
