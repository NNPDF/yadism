Runner
======

The `Runner` class is used to provide a unique entry point to `yadism`
functionalities.

In order to compute any kind of observable a `Runner` instance should be
instantiated, and fed with the proper theory (in the shape of a python
:class:`dict`) and the observables runcard (also as a python :class:`dict`).

.. admonition:: I/O

   Dealing with runcards as files is not a goal of `Runner`, so you can just load
   yourself whatever kind of file format you prefer (`json`, `yaml`, any type of
   db), you just need to manage the conversion step from/into a :class:`dict`.

   Almost in the same way you can/must manage the output as well (an `output
   object`__ is provided, but you can ask instead for a bare :py:class:`dict`,
   or ask the object itself for the equivalent :class:`dict`).

   __ Output_

Handlers objects
----------------

Number of flavours
~~~~~~~~~~~~~~~~~~
Track the use of number of flavours all around in the code.

- number of active (light) flavours
- flavours in input
- flavours in FXlight output
- flavours in internal loops
- FNS

Output
------
The output object bla bla...
