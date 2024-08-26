####################
Yadism documentation
####################

.. image:: /_static/logo-favicon.png
   :align: center

`yadism` is a wonderful 😉 package for computing |DIS| observables.

Citation Policy
~~~~~~~~~~~~~~~

When using our code please cite

- our DOI: |DOI|_
- our paper: |arxiv|_

.. |DOI| image:: https://zenodo.org/badge/219968694.svg
.. _DOI: https://zenodo.org/badge/latestdoi/219968694
.. |arxiv| image:: https://img.shields.io/badge/arXiv-2401.15187-b31b1b?labelColor=222222
.. _arxiv: https://arxiv.org/abs/2401.15187

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

.. toctree::
   :maxdepth: 1
   :caption: Overview
   :hidden:

   overview/features.rst
   overview/tutorials/tutorials.rst

.. toctree::
   :maxdepth: 1
   :caption: Theory
   :hidden:

   theory/intro.rst
   theory/fact.rst
   theory/coeff-funcs.rst
   theory/fns.rst
   theory/scale-variations.rst
   Misc <theory/misc.rst>

   zzz-refs.rst

.. toctree::
   :maxdepth: 1
   :caption: Implementation
   :hidden:

   implementation/structure.rst
   implementation/scale-variations.rst
   implementation/TMC.rst
   API <modules/yadism.rst>
   ui/yadbox.rst

.. toctree::
   :maxdepth: 1
   :caption: Dev Tools
   :hidden:

   dev-tools/benchmarks.rst
   dev-tools/yadmark.rst
   dev-tools/code-todos.rst

.. toctree::
   :maxdepth: 1
   :caption: Navigation
   :hidden:

   overview/indices.rst
