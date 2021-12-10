from . import BCDMS, CHORUS, HERA, NMC, NUTEV, SLAC

exps = {
    getattr(m, "__name__").split(".")[-1]: m
    for m in [CHORUS, HERA, NMC, NUTEV, SLAC, BCDMS]
}
