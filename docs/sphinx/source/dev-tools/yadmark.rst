Yadmark
=======

Here we describe the design and API of the `yadmark` package.
The underlying infrastructure is coming from `sqlite3` and `git-lfs` and it 
is implemented in the package |banana|. 

.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   navigator.rst
   API <yadmark/yadmark.rst>

Available Benchmarks
--------------------

In the ``benchmarks/runners`` we provide a list of established benchmarks

- ``sandbox.py``:

  - it is used to provide the boilerplate needed for a basic run,
    in order to make a quick run for debugging purpose, but still fully managed
    and registered by the `yadmark` machinery and then available in the
    `navigator`

- ``apfel_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |APFEL|
  - the necessary python bindings are provided by the |APFEL| itself

- ``qcdnum_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |QCDNUM|
  - the necessary python bindings are provided by us externally

- ``xspace_bench_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against `xspace-bench`
  - the necessary python bindings are provided by us externally

Furthermore all of them are examples useful to understand how to use the
`yadmark` package for benchmarking.
