r"""
The coefficient functions definition is given in :eqref:`4.2`,
:cite:`vogt-f2nc` (that is the main reference for their expression, i.e. all
the formulas in this module) (the same of :eqref:`1` in :cite:`vogt-flnc`).
The main reference for their expression is :cite:`vogt-flnc`.

Scale varitions main reference is :cite:`nnlo-sv-singlet` and
:cite:`nnlo-sv-nonsinglet`.

Scale variations main reference is :cite:`moch-f3nc`.

Note
----
    *   Check the theory reference for details on
        :doc:`../theory/scale-variations`

    *   The source files (available in fortran) follow the notations in :cite:`vogt-f3cc`
        where the odd-N moments are called minus even if they correspond to :math:`\nu + \bar{\nu}`.
        This convention is changed in :cite:`Davies:2016ruz` where the complete |N3LO| CC results are presented
        for the first time. Referred equations are not always in agreement with the code conventions.

    The code follows the notation:

    F3:
        * odd N: :math:`\nu + \bar{\nu}`, :math:`c_{ns,-}` common for CC and NC (up to N3LO).
        * even N: :math:`\nu - \bar{\nu}`, :math:`c_{ns,+} = \delta + c_{ns,-}` only for CC.
        * In :math:`c_{ns,+}` the term fl02 has to be turned off for CC.

    F2, FL:
        * odd N: :math:`\nu - \bar{\nu}`, :math:`c_{ns,-} = - \delta + c_{ns,+}` only for CC.
        * even N: :math:`\nu + \bar{\nu}`, :math:`c_{ns,+}` common for CC and NC (up to N3LO).
        * The term fl11 has to be turned off for CC.

"""

from . import kernels
