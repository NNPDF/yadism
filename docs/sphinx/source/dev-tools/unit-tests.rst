Unit Tests
==========

Unit tests are provided to test all the components of the package isolated.

Strategy
--------

#. **Minimal:** The setup for each test is kept always minimal, trying to reduce each test to
   its atomic components.
#. **Mocking:** If needed some structures are mocked to be able to run piece of codes the
   depend on the presence of something else.
#. **Errors:** Even the error raising is tested, to ensure its consistency.

Coverage
--------
The testing is checked and guaranteed by coverage metrics.

.. warning::

   The coverage metric used is the one available with the package
   :mod:`pytest`, but it's a little bit naïve.

   Indeed the lines of code explored by tests are watched and reported in a
   very comfortable way, but more involved scenarios are ignored.

   *For example*: if a single line of code will contain a branching (inline
   ``if... else...`` structure) it is considered explored even if not all the
   branches are explored by tests.
