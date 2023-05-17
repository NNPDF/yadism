
Usage
=====

Yadmark mimics the same inputs needed to run `yadism`, namely a theory card, an
observable card and also the name of a pdf set.

Both the theory and observable card can be gnerated authomatically from a default:
the former with |banana|, the latter with something similar to ``generate_observable()`` provided `sandbox.py`.

In addition to run `yadmark` you need to specify the external program you would benchmark against.
To do so, you will have to initialise a class of type ``yadmark.benchmark.runner``.
In the following section we describe some available `runners` which are the most useful example.

The minimal setup of the input cards must contain:

.. list-table:: minimal theory input runcard
  :header-rows: 1

  * - Name
    - Type
    - default
    - description
  * - ``PTO``
    - :py:obj:`int`
    - [required]
    - order of perturbation theory: ``0`` = LO, ...

.. list-table:: minimal observable input runcard
  :header-rows: 1

  * - Name
    - Type
    - default
    - description
  * - ``observable_names``
    - :py:obj:`dict`
    - [required]
    - lsit of SF to be evaluated a the corresponding (x, Q2) ex.: ``['F2light': [{x: 0.1, Q2: 90} ], ... ]``
  * - ``interpolation_xgrid``
    - :py:obj:`lsit(float)`
    - [required]
    - the interpolation grid
  * - ``interpolation_polynomial_degree``
    - :py:obj:`int`
    - [required]
    - polynomial degree of the interpolating function
  * - ``interpolation_is_log``
    - :py:obj:`bool`
    - [required]
    - use logarithmic interpolation?
  * - ``prDIS``
    - :py:obj:`str`
    - [required]
    - DIS current: ``EM``, ``NC``, ``CC``
  * - ``ProjectileDIS``
    - :py:obj:`str`
    - [required]
    - DIS projectile

The output of `yadmark` will be stored in ``data/benchmark.db`` inside a :py:obj:`Pandas.DataFrame` table.
You can then use the :doc:`navigator<navigator>` app to inspect your database.

Available Runners
-----------------

In ``benchmarks/runners`` we provide a list of established benchmarks

- ``sandbox.py``:

  - it is used to provide the boilerplate needed for a basic run,
    in order to make a quick run for debugging purpose, but still fully managed
    and registered by the `yadmark` machinery and then available in the
    `navigator`

- ``apfel_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |APFEL|. The complete
    run of this script will benchmark yadism against all the compatible |APFEL| features.
  - the necessary python bindings are provided by the |APFEL| itself

- ``qcdnum_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |QCDNUM|. The complete
    run of this script will benchmark yadism against all the compatible |QCDNUM| features.
  - the necessary python bindings are provided by us externally

- ``xspace_bench_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |xspace-bench|. The complete
    run of this script will benchmark yadism against all the compatible |xspace-bench| features.
  - the necessary python bindings are provided by us externally

- ``apfelpy_bench.py``:

  - it is used by the corresponding workflow to
    run the established benchmarks against |APFEL++|. The complete
    run of this script will benchmark yadism against all the compatible |APFEL++| features.
  - the necessary python bindings are provided by the |APFEL++| itself

All of them are examples useful to understand how to use the
`yadmark` package for benchmarking.
