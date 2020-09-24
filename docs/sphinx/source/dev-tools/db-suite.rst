Database Test Suite
===================

We developed a test suite to manage the several configuration to be tested
through a proper database (currently implemented on `tinydb`).

The suite currently consists of:

.. todo::

   Update with the current structure

- some scripts able to fill an **input database** (filling includes creating it,
  if does not exist yet)
- a **navigator**, able to display the content of both the *input database*,
  and the output one, to store the data generated during test process itself

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

.. _document-oriented: https://en.wikipedia.org/wiki/Document-oriented_database
.. _json: https://it.wikipedia.org/wiki/JavaScript_Object_Notation

Git LFS
-------

In order to keep the databases in the projects we decided to use `git-lfs`
(`git` Large File Storage), a tool integrating with `git` and designed
specifically to manage large files inside a `git` repo.
