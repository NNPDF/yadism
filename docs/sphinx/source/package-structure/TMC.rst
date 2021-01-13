Target Mass Corrections
=======================



Work in Progress notes
----------------------


Runner: holds a list of structure functions instances, that will act as our
"soft singletons"
StructureFunction: holds a reference to his parent runner, in this way its also
able to access its StructureFunctions siblings (like F2 from FL, in order to
compute TMCs, e.g.)

Caching: it is managed at the level of StructureFunction, while the values are
kept at the level of ESF (so the StructureFunction is just routing the caller to
the correct instance of ESF to ask for values)

Note 2 (caching)
----------------
Since the responsibility of caching is of SF as written above we decided the
following layout:

- SF instantiate ESF or ESFTMC according to TMC flag in theory dictionary,
  and append it to `self.__ESFs` at load time, i.e. in `self.load()` (these
  are the observables to be computed)
- when asked for output if noTMC a ESF is called and the instance is
  registered

    - `self.get_ouput()` is used for getting the result passing through:
    - `self.get_ESF()` is used for getting the instance and register to the
      cache

- if TMC a ESFTMC is called, and whenever he needs an ESF instance to
  compute a point it will ask its parent SF with `SF.get_ESF()` method, in
  this way passing through the cache