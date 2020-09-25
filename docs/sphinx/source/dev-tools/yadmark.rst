Yadmark
=======

.. Important::
   
   In this section is described the design and API of the `yadmark` package.
   The underlying infrastructure is coming from `tinydb` and `git-lfs`, and it
   is briefly explained in :doc:`db-suite`.

.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   benchmark-runner.rst
   navigator.rst
   API <yadmark/yadmark.rst>

Runners
-------

Some runner scripts are provided in the ``benchmarks/runners`` folder for
different purposes.

- ``sandbox.py``: it is used to provide the boilerplate needed for a basic run,
  in order to make a quick run for debugging purpose, but still fully managed
  and registered by the `yadmark` machinery and then available in the
  `navigator`
- ``regression.py``: it is used manually and by the corresponding workflow to
  run the regression tests (see :doc:`regression-tests`) 
- ``benchmarks_against_apfel.py``: it is used by the corresponding workflow to
  run the established benchmarks against |APFEL|, and verify the agreement or the
  known differences between the two results
- ``benchmarks_against_qcdnum.py``: same as the previous one for |QCDNUM|

Furthermore all of them are examples useful to understand how to use the
`yadmark` package for benchmarking.
