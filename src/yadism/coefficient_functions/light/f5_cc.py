from ..partonic_channel import RSL
from . import partonic_channel as pc

# At LO, only the Non-Singlet part is non-zero and is proportional to
# `delta`. Starting at NLO, the Gluon part starts to contribute.


class NongSinglet(pc.LightBase):
    @staticmethod
    def LO():
        return RSL.from_delta(1.0)
