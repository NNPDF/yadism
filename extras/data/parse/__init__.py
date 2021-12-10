from . import BCDMS, CHORUS, HERA, NUTEV, SLAC

exps = {
    getattr(m, "__name__").split(".")[-1]: m for m in [CHORUS, HERA, NUTEV, SLAC, BCDMS]
}
