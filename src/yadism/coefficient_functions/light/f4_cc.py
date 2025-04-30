from .. import partonic_channel as epc

# In the massless limit, F4 vanishes both at LO and NLO.
# Only when heavy quark masses are accounted for that its
# contribution is non-zero.


class Gluon(epc.EmptyPartonicChannel):
    pass


class Singlet(epc.EmptyPartonicChannel):
    pass


class Valence(epc.EmptyPartonicChannel):
    pass
