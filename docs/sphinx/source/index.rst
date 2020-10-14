.. DIS documentation master file.


####################
Yadism documentation
####################

.. the following transition is only used for highlight the main title

---------

`yadism` is a wonderful package for computing |DIS| observables replacing the
corresponding one inside |APFEL|.

Features
~~~~~~~~

**Features** already implemented include:

- |LO| structure functions
- |NLO| structure functions

  1. scale variations
  2. target mass corrections
  3. flavor number schemes

The implemented structure functions are :math:`F_2,~F_L,~F_3` for the following
|DIS| processes:

- |EM|
- |NC|
- |CC|

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   yadism.rst
   tutorials/index.rst

In these :underlined:`documents` you can find the reference for all *yadism* API and internals.

.. toctree::
   :maxdepth: 1
   :caption: Theory

   theory/DIS-intro.rst
   theory/coeff-funcs.rst 
   theory/light-flavors.rst
   theory/heavy-flavors.rst
   theory/processes.rst
   theory/scale-variations.rst
   theory/TMC.rst

   zzz-refs.rst

And here there is some *physics documentation*.

Some of these are trivial and will be replaced, they are here just to create a
structure.


.. toctree::
   :maxdepth: 1
   :caption: Dev Tools

   dev-tools/tests.rst
   dev-tools/db-suite.rst
   dev-tools/yadmark.rst
   dev-tools/extras.rst
   dev-tools/third-party.rst
   dev-tools/code-todos.rst

These tools have been developed alongside `yadism`, in order to automatize tests
and improve the quality of code (less bugs, more readable... hopefully...).

---------


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
