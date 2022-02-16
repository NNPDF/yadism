# -*- coding: utf-8 -*-
import numpy as np

from . import fonll, heavy, intrinsic, kernels, light
from .partonic_channel import EmptyPartonicChannel


class Component(list):
    """
    Used for organize elements and debugging purpose.
    """

    heavyness = {0: "light", 4: "charm", 5: "bottom", 6: "top"}

    def __init__(self, heavy, kernels=None):
        self.heavy = self.heavyness[heavy]

        if kernels is None:
            kernels = []
        super().__init__(kernels)

    def __repr__(self):
        return self.heavy + f"({len(self)} kernels)"


# TODO add more doc strings


class Combiner:
    """
    Does the matching between coefficient functions and partons with their approptiate coupling
    strength.

    Parameters
    ----------
        esf : EvaluateStructureFunction
            current ESF
    """

    def __init__(self, esf):
        self.esf = esf
        self.masses = {4 + i: not mass for i, mass in enumerate(esf.info.ZMq)}
        self.intrinsic = esf.info.intrinsic_range
        self.obs_name = esf.info.obs_name
        self.nf = esf.info.threshold.nf(esf.Q2)
        self.target = esf.info.target

    def collect(self):
        comps = []

        family = self.obs_name.flavor_family

        # Adding light component
        if family in ["light", "total"]:
            comps.append(self.light_component())
        if family == "heavy":
            #  the only case in which an heavy contribution is not present in those
            #  accounted for in total, it's whene heavy already became heavylight
            comps.extend(self.heavylight_components())
        if family in ["heavy", "total"]:
            comps.extend(self.heavy_components())

        return comps

    def light_component(self):
        nf = self.nf
        masses = self.masses

        comp = Component(0)

        # the first condition essentially checks nf != 3
        if nf in masses and masses[nf]:
            nl = nf - 1
            comp.extend(
                fonll.kernels.generate_light(
                    self.esf, nl, self.esf.info.theory["pto_evol"]
                )
            )
            comp.extend(heavy.kernels.generate_missing(self.esf, nl, nl + 1))
            comp.extend(
                self.damp_elems(
                    nl,
                    fonll.kernels.generate_light_diff(
                        self.esf,
                        nl,
                        self.esf.info.theory["pto_evol"],
                    ),
                )
            )
        else:
            comp.extend(light.kernels.generate(self.esf, nf))

        for ihq in range(nf + 1, 7):
            if masses[ihq]:
                comp.extend(heavy.kernels.generate_missing(self.esf, nf, ihq))
        return comp

    def heavylight_components(self):
        nf = self.nf
        hq = self.obs_name.hqnumber
        masses = self.masses

        comps = []

        if hq < nf or (hq == nf and not masses[hq]):
            heavylight = Component(hq)
            heavylight.extend(kernels.generate_single_flavor_light(self.esf, nf, hq))
            comps.append(heavylight)

        return comps

    def heavy_components(self):
        nf = self.nf
        hq = self.obs_name.hqnumber
        masses = self.masses

        comps = []

        heavy_comps = {}
        for sfh in range(nf, 7):
            # exclude sfh=3, since heavy contributions are there for [4,5,6]
            # if it's ZM you don't even have the component
            if sfh not in masses or not masses[sfh]:
                continue

            heavy_comps[sfh] = Component(sfh)
            if hq not in (0, sfh):
                continue

            if sfh == nf:
                # then it is FONLL
                nl = nf - 1
                heavy_comps[sfh].extend(heavy.kernels.generate(self.esf, nl, ihq=sfh))
                if sfh not in self.intrinsic:
                    heavy_comps[sfh].extend(
                        self.damp_elems(
                            nl,
                            fonll.kernels.generate_heavy_diff(
                                self.esf, nl, self.esf.info.theory["pto_evol"]
                            ),
                        )
                    )
                else:
                    heavy_comps[sfh].extend(
                        intrinsic.kernels.generate(self.esf, ihq=sfh)
                    )
                    heavy_comps[sfh].extend(
                        self.damp_elems(
                            nl,
                            fonll.kernels.generate_heavy_intrinsic_diff(
                                self.esf, nl, self.esf.info.theory["pto_evol"]
                            ),
                        )
                    )
            else:
                # then it is *not* FONLL
                heavy_comps[sfh].extend(heavy.kernels.generate(self.esf, nf, ihq=sfh))
                if sfh in self.intrinsic:
                    heavy_comps[sfh].extend(
                        intrinsic.kernels.generate(self.esf, ihq=sfh)
                    )

            for ihq in range(sfh + 1, 7):
                if masses[ihq]:
                    heavy_comps[sfh].extend(
                        heavy.kernels.generate_missing(self.esf, nf, ihq, icoupl=sfh)
                    )
            comps.append(heavy_comps[sfh])

        return comps

    def damp_elems(self, nl, elems):
        """
        Damp FONLL difference contributions if necessary.

        Parameters
        ----------
            nl : int
                number of *light* flavors
            elems : list(Kernel)
                kernels to be modified

        Returns
        -------
            elems : list(Kernel)
                modified kernels
        """
        if not self.esf.info.FONLL_damping:
            return elems
        nhq = nl + 1
        # TODO: replace mass with threshold?
        m2hq = self.esf.info.m2hq[nhq - 4]
        power = self.esf.info.damping_powers[nhq - 4]
        if self.esf.Q2 > m2hq:
            damp = np.power(1.0 - m2hq / self.esf.Q2, power)
        else:
            damp = 0.0
        return (damp * e for e in elems)

    @staticmethod
    def apply_isospin(full, z, a):
        """
        Apply isospin symmetry to u and d distributions.

        Parameters
        ----------
            full : list(yadism.kernels.Kernel)
                all participants
            z : float
                number of protons
            a : float
                atomic mass number
        """
        nucl_factors = np.array([[z, a - z], [a - z, z]]) / a
        for ker in full:
            for sign in [-1, 1]:
                ps = np.array(
                    [ker.partons.get(sign * 1, 0), ker.partons.get(sign * 2, 0)]
                )
                ker.partons[sign * 1], ker.partons[sign * 2] = nucl_factors @ ps

    @staticmethod
    def drop_empty(full):
        """
        Drop kernels with :class:`EmptyPartonicChannel` or its partons with empty weight.

        Parameters
        ----------
            elems : list(yadism.kernels.Kernel)
                all participants

        Returns
        -------
            filtered_kernels : list(yadism.kernels.Kernel)
                improved participants
        """
        filtered_kernels = []
        for ker in full:
            ker.partons = {p: w for p, w in ker.partons.items() if w != 0}
            if len(ker.partons) > 0 and not isinstance(ker.coeff, EmptyPartonicChannel):
                filtered_kernels.append(ker)
        return filtered_kernels

    def collect_elems(self):
        """
        Collects all kernels according to the |FNS|.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants
        """
        components = self.collect()

        full = []
        for comp in components:
            full.extend(comp)

        # add level-0 nuclear correction: apply isospin symmetry
        self.apply_isospin(full, self.target["Z"], self.target["A"])

        # drop all kernels with 0 weight, or empty coeffs
        return self.drop_empty(full)
