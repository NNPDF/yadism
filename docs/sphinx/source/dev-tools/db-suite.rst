Database Test Suite
===================

We developed a test suite to manage the several configuration to be tested
through a proper database (currently implemented on `tinydb`).

The suite currently consists of:

- some scripts able to fill an **input database** (filling includes creating it,
  if does not exist yet)
- a **navigator**, able to display the content of both the *input database*,
  and the output one, to store the data generated during test process itself

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


Navigator
---------
Enter through the entry script `navigator` running:
```shell
./navigator
```
in `benchmarks` folder.

The script will load the full interface and drop into an `ipython` interpreter
instance, so the interface is available as a set of python functions.
Once inside the interpreter all the functions in:

- the interface
- `pylab`

will be available without any prefix (they are imported in the global namespace).

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

Database infrastructure
-----------------------
In the current version databases are managed through `tinydb`, a DBMS
implemented as a python package, that makes it easier to interface with
python-based tests, and also gave us the chance to deploy the whole generation
ecosystem and navigator in python itself.

Since `tinydb` is used the databases are document-oriented_, that also makes
them more flexible and easier to manage less homogeneous data.

The databases themselves consist of a single json_ file per db, and this makes
it very easy to store, transfer and manage. No system-wide installation is
needed to interact with the db, and can be easily sent around since it is a
bare text file, nothing more than formatted.

In principle it is always possible to explore the file content through any text
editor, but in order to save space (and since it is designed to be managed by a
proper tool) the readability its reduced because of lack of whitespaces, and
the presence of internal structures.
If needed it can be simply reformatted adding automatically whitespaces, but
when available its always better to interact with it through the proper
manager.

.. _document-oriented: https://en.wikipedia.org/wiki/Document-oriented_database
.. _json: https://it.wikipedia.org/wiki/JavaScript_Object_Notation
