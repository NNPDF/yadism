Yadmark
=======

Here we describe the design and API of the `yadmark` package.
The specific purpose of this package is to cointain all the utils to benchmark efficiently Yadism. 
The underlying infrastructure is coming from `sqlite3` and `git-lfs` and it 
is implemented in the package |banana|.
To run Yadmark see the section below of the available runners. 
Furthermore Yadmark provide also a python interpter called `navigator` to inspect the cached benchmark reuslts. 

.. toctree::
   :maxdepth: 1

   navigator.rst
   API <yadmark/yadmark.rst>

Available Runners
-----------------

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

All of them are examples useful to understand how to use the
`yadmark` package for benchmarking.
