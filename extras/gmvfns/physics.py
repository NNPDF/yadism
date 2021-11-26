from .elements import VFNS, Component, KernelGroup, Patch


def combiner(obs, nf, confs):
    p = Patch(obs, nf)

    light = Component("light")

    p.append(light)
    return p


def scan(confs):
    vfns = VFNS(confs)

    for nf in range(3, 7):
        vfns.append(combiner(confs.obs, nf, confs))

    return vfns
