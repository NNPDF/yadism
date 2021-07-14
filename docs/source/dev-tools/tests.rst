Tests
=====

.. admonition:: Abstract

   In this section you will find an abstract description of the tests
   implemented in `yadism`, while the concrete facility is implemented in
   `yadmark` package and described in :doc:`yadmark`.

Multiple kinds of tests are provided with the packages, that will guarantee the
desired behavior is the one implemented.

Tests are run by |CI|, the elected system is |gh-act| (because of the
simplicity to manage it from the repo already hosted on GitHub).

.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   unit-tests.rst
   regression-tests.rst
   benchmarks.rst
   profiling.rst
