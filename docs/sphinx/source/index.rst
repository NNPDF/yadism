.. DIS documentation master file.


####################
Yadism documentation
####################

.. the following transition is only used for highlight the main title

---------

`yadism` is a wonderful package for computing |DIS| observables replacing the
corresponding one inside |APFEL|.

Design Goals
~~~~~~~~~~~~

`yadism` present some real advantages with respect to analogous codes
available. They are mainly related to the choice of developing this project
applying a modern methodology.

In particular:

- the project is open source, freely available from an early stage of
  development, open for requests and contributions
- the project has been developed using *python*, because even if it would make
  harder to improve the runtime performances, it will improve enormously
  readability

  - the performances issues are delegated to the use of external compiled
    extensions (like scipy_), relying on very well tested libraries, or even
    using JIT compiled code (or in general python defined compiled code), e.g.
    using numba_

    .. code-block:: shell

       pip install yadism

- another great benefit of the previous point is the delivering and
  portability: the project is deployed on PyPI_ and you can simply download it
  using pip_, simply running:
- the project is managed applying CI/CD patterns, in this way is continuously
  benchmarked at any update, against other tools, itself and preserving
  invariants exploiting a unit-test suite (for a full description see
  :doc:`dev-tools/tests`)
- a lot of attention has been paid in writing a helpful and detailed
  documentation, to help users and future maintainers

.. _scipy: https://scipy.org/
.. _numba: http://numba.pydata.org/
.. _PyPI: https://pypi.org/project/yadism/
.. _pip: https://pip.pypa.io/en/stable/

Features
~~~~~~~~

**Features** already implemented include:

- |LO| structure functions
- |NLO| structure functions

  1. scale variations
  2. target mass corrections
  3. flavor number schemes

The implemented structure functions are :math:`F_2,~F_L,~F_3` for the following
|DIS| processes:

- |EM|
- |NC|
- |CC|

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   yadism.rst
   tutorials/index.rst

In these :underlined:`documents` you can find the reference for all *yadism* API and internals.

.. toctree::
   :maxdepth: 1
   :caption: Theory

   theory/DIS-intro.rst
   theory/structure-functions.rst
   theory/coeff-funcs.rst 
   theory/light-flavors.rst
   theory/heavy-flavors.rst
   theory/processes.rst
   theory/scale-variations.rst
   theory/TMC.rst

   zzz-refs.rst

And here there is some *physics documentation*.

Some of these are trivial and will be replaced, they are here just to create a
structure.


.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   dev-tools/tests.rst
   dev-tools/db-suite.rst
   dev-tools/yadmark.rst
   dev-tools/extras.rst
   dev-tools/third-party.rst
   dev-tools/code-todos.rst

These tools have been developed alongside `yadism`, in order to automatize tests
and improve the quality of code (less bugs, more readable... hopefully...).

---------


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
