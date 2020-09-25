Benchmark Runner
================

.. todo::

   It is not anymore an ecosystem of scripts but a proper object-oriented
   python subpackage.

   - update the status
   - describe the description of the API (how the user can interact with the
     runner itself)
   - describe the current design

Generating Ecosystem
--------------------
It currently consists of some scripts able to iterate properly over the
options, generating each one a table in input database `input.json`.
Each combination defined is stored in one record of the suitable table that
makes it easier to iterate over them and query the options.

The current scripts are:

- `theories.py`: create the table `theories` (purging any existing one, if
  already exists)
- `observables.py`: create the table `observables` (purging any existing one,
  if already exists)
- `observables-regression.py`: create the table `observables-regression`
  (purging any existing one, if already exists)


I/O databases' structure
------------------------

Input database will consist of the tables:

- **theories**: each entry of this table will represent a *physical theory*,
  i.e. it will specify a set of parameters involved in QFT computations; the
  following entries are expected:

  - *PTO*: perturbative order
  - *XIF*, *XIR*: 
  - *mc*. *Qmc*, *mb*, *Qmb*, *mt*, *Qmt*:
  - ...

- **observables**: each entry of this table will represent a *set of DIS
  observables*, and also some parameters involved in the computation of the
  observables themselves; the following entries are expected:

  - *xgrid*: the grid on which the interpolation is evaluated 
  - ...

- **observables-regression**: this table is completely analogous to the
  *observables* one, and uniform in entry format; the difference it is in the
  aim: it is used to define the observables used for *regression tests*, while
  the previous is used in benchmarks (and it is expected to change faster than
  this one)

Output database will consist of the tables:

- **apfel_cache**: to keep a cache of APFEL runs, since APFEL it is stable
  there is no need of rerunning it multiple times to compute the same
  observables (while rerunning is needed for *yadism* during its development,
  of course...)
- **logs**: keep a log of the runs of *yadism*


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
