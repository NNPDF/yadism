Regression Tests
================

This tests are implemented to guarantee the historical consistency of
:mod:`yadism` results.

Description
-----------

A set of results is produced at a given time and stored separately from the
package code (currently a *GitHub Gist* has been chosen for storing the
``json`` file).

The regression runner will run the same calculation with the same settings of
the previously generated results, fetch these ones and compare the new with the
stored to ensure that nothing has been changed (if some behavior has been
modified willfully it will be sufficient to ignore the generated warning).


Slicing (1-hot)
---------------

Since it is not possible to test the full matrix of combinations, because of
its exponential complexity in the features number, a one-hot strategy has been
adopted.

.. admonition:: 1-hot

   It means that if multiple features can be toggle a single one is chosen and
   activated, keeping all the others off. Then iterate over all the possible
   selection (we borrowed this name from the well-known `One-hot encoding
   <https://en.wikipedia.org/wiki/One-hot>`_.

This means that **all the features** are controlled by the *regression tests*,
but **not all the combinations**.
