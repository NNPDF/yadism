# -*- coding: utf-8 -*-
"""
Runner: holds a list of structure functions instances, that will act as our
"soft singletons"
StructureFunction: holds a reference to his parent runner, in this way its also
able to access its StructureFunctions siblings (like F2 from FL, in order to
compute TMCs, e.g.)

Caching: it is managed at the level of StructureFunction, while the values are
kept at the level of ESF (so the StructureFunction is just routing the caller to
the correct instance of ESF to ask for values)

Note 1
------
Here is the third time that we are proliferating the SF classes to all the
flavours and kinds (SF/ESFTMC/ESF x 2/L x light/c/b/t), but at the bottom level
they are needed (ESF implementation are actually different for every option, so
it makes sense to have different classes).
The classes one level above (SF/ESFTMC) are simply shadowing the ones below in
order to route to the correct one. The same business can be done with a `switch`
pattern (actually `if...elif...elif...` in python), but the only difference is
how many lines of code you are saving.
**Proposal** for a better layout in which we don't need to explicitly shadow
from level to level (and we don't need to route with `if` as well) are liked and
likeòy to be accepted.

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

.. todo::
    docs
"""
import abc

import numpy as np


class EvaluatedStructureFunctionTMC(abc.ABC):
    def __init__(self, SF, kinematics):
        self._SF = SF
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]

        self._rho = np.sqrt(1 + 4 * self._x ** 2 * self._SF._M2target / self._Q2)
        self._xi = 2 * self._x / (1 + self._rho)


class ESFTMC_F2(EvaluatedStructureFunctionTMC):
    def __init__(self, SF, kinematics, ESF):
        super(ESFTMC_F2, self).__init__(SF, kinematics)
        self._ESF = ESF


class ESFTMC_FL(EvaluatedStructureFunctionTMC):
    def __init__(self, SF, kinematics, ESF):
        super(ESFTMC_FL, self).__init__(SF, kinematics)
        self._ESF = ESF
