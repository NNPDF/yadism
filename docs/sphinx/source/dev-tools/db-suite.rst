Database Test Suite
===================

We developed a test suite to manage the several configuration to be tested
through a proper database (currently implemented on `tinydb`).

The suite currently consists of:

.. todo::

   Update with the current structure

- a **navigator**, able to display the content of both the *input database*,
  and the output one, to store the data generated during test process itself
- `generate_theories`: create the table `theories` (purging any existing one, if
  already exists)
- `generate_observables`: create the table `observables` (purging any existing one,
  if already exists)

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

.. _document-oriented: https://en.wikipedia.org/wiki/Document-oriented_database
.. _json: https://en.wikipedia.org/wiki/JavaScript_Object_Notation

I/O databases' structure
""""""""""""""""""""""""

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

- **apfel_cache/qcdnum_cache/regression**: to keep a cache of the external output. Since it is stable
  there is no need of rerunning it multiple times to compute the same
  observables (while rerunning is needed for *yadism* during its development,
  of course...)

Output database will consist of the tables:

- **logs**: keep a log of the comparisons between *yadism* and the external program

(Little) human readability
""""""""""""""""""""""""""

In principle it is always possible to explore
the file content through any text editor, but in order to save space (and since
it is designed to be managed by a proper tool) the readability its reduced
because of lack of whitespaces, and the presence of internal structures.

If needed it can be simply reformatted adding automatically whitespaces, but
when available its always better to interact with it through the proper
manager (consider also that is a **huge** text file, that can break simple
editors trying to load all at once).

Git LFS
-------

In order to keep the databases in the projects we decided to use git-lfs_
(`git` Large File Storage), a tool integrating with `git` and designed
specifically to manage large files inside a `git` repo.

.. _git-lfs: https://git-lfs.github.com