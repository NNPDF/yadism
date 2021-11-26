from .elements import VFNS, Component, KernelGroup, Patch


def combiner(obs, nf, masses):
    p = Patch(obs, nf)

    light = Component(0)
    if nf in masses and masses[nf]:
        light.append(KernelGroup("light", nf, ihq=nf, fonll=True))
    else:
        light.append(KernelGroup("light", nf))

    for ihq in range(nf + 1, 7):
        if masses[ihq]:
            light.append(KernelGroup("miss", nf, ihq=ihq))

    p.append(light)
    return p


def scan(confs):
    vfns = VFNS(confs)

    for nf in range(3, 7):
        vfns.append(combiner(confs.obs, nf, vfns.masses))

    return vfns
