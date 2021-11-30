from .elements import VFNS, Component, KernelGroup, Patch


def combiner(obs, nf, masses):
    p = Patch(obs.name, nf)

    # Adding light component
    if obs.family in ["light", "total"]:
        light = Component(0)
        # the first condition essentially checks nf != 3
        if nf in masses and masses[nf]:
            light.append(KernelGroup("light", nf, ihq=nf, fonll=True))
        else:
            light.append(KernelGroup("light", nf))

        for ihq in range(nf + 1, 7):
            if masses[ihq]:
                light.append(KernelGroup("miss", nf, ihq=ihq, nc=nf))

        p.append(light)
    if obs.family == "heavy":
        #  the only case in which an heavy contribution is not present in those
        #  accounted for in total, it's whene heavy already became heavylight
        if obs.hq < nf or (obs.hq == nf and not masses[obs.hq]):
            heavylight = Component(obs.hq)
            heavylight.append(KernelGroup("light", nf, ihq=obs.hq, nc=1))
            p.append(heavylight)
    if obs.family in ["heavy", "total"]:
        heavy = {}
        for sfh in range(nf, 7):
            # if it's ZM you don't even have the component
            # exclude sfh=3, since heavy contributions are there for [4,5,6]
            if sfh in masses and masses[sfh]:
                heavy[sfh] = Component(sfh)
                if obs.hq != 0 and obs.hq != sfh:
                    continue

                if sfh == nf:
                    heavy[sfh].append(KernelGroup("heavy", nf, ihq=sfh, fonll=True))
                else:
                    heavy[sfh].append(KernelGroup("heavy", nf, ihq=sfh))

                for ihq in range(sfh + 1, 7):
                    if masses[ihq]:
                        heavy[sfh].append(KernelGroup("miss", nf, ihq=ihq, nc=1))
                p.append(heavy[sfh])
    return p


def scan(confs):
    vfns = VFNS(confs)

    for nf in range(3, 7):
        vfns.append(combiner(vfns.obs, nf, vfns.masses))

    return vfns
