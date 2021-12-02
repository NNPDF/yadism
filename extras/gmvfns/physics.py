from .elements import VFNS, Component, KernelGroup, Patch


def light_component(nf, masses):
    comp = Component(0)
    # the first condition essentially checks nf != 3
    if nf in masses and masses[nf]:
        comp.append(KernelGroup("light", nf, fonll=True))
    else:
        comp.append(KernelGroup("light", nf))

    for ihq in range(nf + 1, 7):
        if masses[ihq]:
            comp.append(KernelGroup("miss", nf, ihq=ihq, nc=nf))
    return comp


def heavylight_components(nf, hq, masses):
    comps = []
    if hq < nf or (hq == nf and not masses[hq]):
        heavylight = Component(hq)
        heavylight.append(KernelGroup("light", nf, ihq=hq, nc=1))
        comps.append(heavylight)

    return comps


def heavy_components(nf, hq, masses):
    comps = []
    heavy = {}
    for sfh in range(nf, 7):
        # if it's ZM you don't even have the component
        # exclude sfh=3, since heavy contributions are there for [4,5,6]
        if sfh in masses and masses[sfh]:
            heavy[sfh] = Component(sfh)
            if hq != 0 and hq != sfh:
                continue

            if sfh == nf:
                heavy[sfh].append(KernelGroup("heavy", nf, fonll=True))
            else:
                heavy[sfh].append(KernelGroup("heavy", nf, ihq=sfh))

            for ihq in range(sfh + 1, 7):
                if masses[ihq]:
                    heavy[sfh].append(KernelGroup("miss", nf, ihq=ihq, nc=1))
                comps.append(heavy[sfh])

    return comps


def combiner(obs, nf, masses):
    p = Patch(obs.name, nf)

    # Adding light component
    if obs.family in ["light", "total"]:
        p.append(light_component(nf, masses))
    if obs.family == "heavy":
        #  the only case in which an heavy contribution is not present in those
        #  accounted for in total, it's whene heavy already became heavylight
        p.extend(heavylight_components(nf, obs.hq, masses))
    if obs.family in ["heavy", "total"]:
        p.extend(heavy_components(nf, obs.hq, masses))

    return p


def scan(confs):
    vfns = VFNS(confs)

    for nf in range(3, 7):
        vfns.append(combiner(vfns.obs, nf, vfns.masses))

    return vfns
