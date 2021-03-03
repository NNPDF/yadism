Navigator
=========

This app is meant to inspect and comapre `yadism` output versus the external one.

To enter in the `navigator` simply running ``navigator`` command, installed with
the `yadmark` package.

The script will load the full interface and drop into an `ipython` interpreter
instance, so the interface is available as a set of python functions.
Once inside the interpreter all the functions in:

- the interface
- `pylab`

will be available without any prefix (they are imported in the global namespace).
You can aslo type ``h()`` or ``yelp()`` for help.

.. list-table:: Available variables
  :header-rows: 1

  * - Name
    - description
  * - ``t``, ``"theory"``
    -  identifier for all the stored theory cards
  * - ``o``, ``"observable"``
    - identifier for the stored observable cards
  * - ``l``, ``"logs"``
    - identifier for the logs table
  * - ``c``, ``"cache"``
    - identifier for the cached tables


.. list-table:: Available functions
  :header-rows: 1

  * - Name
    - Input
    - description
  * - ``ext(external)``
    - :py:obj:`str`
    - change external
  * - ``g(tbl,id)``
    - :py:obj:`str`, :py:obj:`hash`
    - get all the ``tbl`` tables containing a given ``id``
  * - ``ls(tbl)``
    - :py:obj:`str`
    - list all the ``tbl`` tables with reduced informations
  * - ``dfl(id)``
    - :py:obj:`hash`
    - print the log as DataFrame
  * - ``simlogs(id)``
    - :py:obj:`hash`
    -  find similar logs
  * - ``diff(id, id)``
    - :py:obj:`hash`, :py:obj:`hash`
    - subtract the logs tables
  * - ``comapare(id,id)``
    - :py:obj:`hash`, :py:obj:`hash`
    - compare externals tables 
  * - ``check_log(id)``
    - :py:obj:`hash`
    - check logs passed
  * - ``crashed_log(id)``
    - :py:obj:`hash`
    - print crashed logs

Note that whenever the identifier is unique also part of the full hash or vairiable can be enough to select the corresponding items: 
for istance to call ``dfl("fe4523")`` you can also use ``dfl("fe")`` if in your datababse there are no other hashes containing ``"fe"``. 