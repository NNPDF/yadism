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
        self.heavy = heavy

        if kernels is None:
            kernels = []
        self.extend(kernels)

    def __repr__(self):
        return self.heavy + f"({', '.join(self)})"


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
        self.masses = {4: True, 5: False, 6: False}
        self.obs_name = esf.info.obs_name
        self.nf = esf.info.threshold.nf(esf.Q2)
        self.target = esf.info.target

    def collect(self):
        elems = []

        family = self.obs_name.flavor_family

        # Adding light component
        if family in ["light", "total"]:
            elems.append(self.light_component())
        if family == "heavy":
            #  the only case in which an heavy contribution is not present in those
            #  accounted for in total, it's whene heavy already became heavylight
            elems.extend(self.heavylight_components())
        if family in ["heavy", "total"]:
            elems.extend(self.heavy_components())

        return elems

    def light_component(self):
        nf = self.nf
        nl = self.nf - 1
        masses = self.masses

        comp = Component(0)

        # the first condition essentially checks nf != 3
        if nf in masses and masses[nf]:
            comp.extend(fonll.kernels.generate_light(self.esf, nl))
            comp.extend(
                self.damp_elems(nl, fonll.kernels.generate_light_diff(self.esf, nl))
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
        nl = self.nf - 1
        hq = self.obs_name.hqnumber
        masses = self.masses

        comps = []

        heavy_comps = {}
        for sfh in range(nf, 7):
            # if it's ZM you don't even have the component
            # exclude sfh=3, since heavy contributions are there for [4,5,6]
            if sfh in masses and masses[sfh]:
                heavy_comps[sfh] = Component(sfh)
                if hq != 0 and hq != sfh:
                    continue

                if sfh == nf:
                    heavy_comps[sfh].extend(
                        heavy.kernels.generate(self.esf, nl, ihq=sfh)
                    )
                    heavy_comps[sfh].extend(
                        self.damp_elems(
                            nl, fonll.kernels.generate_heavy_diff(self.esf, nl)
                        )
                    )

                else:
                    heavy_comps[sfh].extend(
                        heavy.kernels.generate(self.esf, nl, ihq=sfh)
                    )

                for ihq in range(sfh + 1, 7):
                    if masses[ihq]:
                        heavy_comps[sfh].extend(
                            heavy.kernels.generate_missing(self.esf, nf, ihq)
                        )
                    comps.append(heavy_comps[sfh])

        return comps

    def collect_fonll(self):
        """
        Collects all kernels for |FONLL|.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants

        Note
        ----
            While we're faking in |FFNS| "lower" heavy structure functions with light with a
            single flavor (e.g. F2c in FFNS5), we do not repeat this here (for the moment).
            We would need to convert the light input into a single flavor input, which would
            in turn increase the complexity of this method.
        """
        elems = []
        # above the *next* threshold use ZM-VFNS
        # nl = self.esf.info.nf_ff - 1
        # if nl + 1 < self.nf:
        #     return self.collect_zmvfns()
        nl = self.nf - 1
        # below charm it is simply FFNS

        if self.obs_name.flavor in ["light", "total"]:
            # FFNSlow
            elems.extend(fonll.kernels.generate_light(self.esf, nl))
            # add F^d
            elems.extend(
                self.damp_elems(nl, fonll.kernels.generate_light_diff(self.esf, nl))
            )
        if self.obs_name.flavor_family in ["heavy", "total"]:
            ihq = nl + 1
            if self.obs_name.is_raw_heavy and self.obs_name.hqnumber < ihq:
                raise NotImplementedError(
                    f"We're not providing {self.obs_name} in FONLL with {nl} light flavors"
                    f"(Q2={self.esf.Q2}) yet"
                )
            # F2b is not avaible in FONLL@c
            if self.obs_name.is_raw_heavy and self.obs_name.hqnumber > ihq:
                raise ValueError(
                    f"{self.obs_name} is not available in FONLL with {nl} light flavors"
                    f"(Q2={self.esf.Q2}) since we're not providing two masses corrections"
                )

            # FFNSlow
            elems.extend(heavy.kernels.generate(self.esf, nl))
            # add F^d
            if ihq in self.esf.info.intrinsic_range:
                elems.extend(intrinsic.kernels.generate(self.esf, ihq))
                elems.extend(
                    self.damp_elems(
                        nl,
                        fonll.kernels.generate_heavy_intrinsic_diff(self.esf, nl),
                    )
                )
            else:
                elems.extend(
                    self.damp_elems(nl, fonll.kernels.generate_heavy_diff(self.esf, nl))
                )
        return elems

    # def collect_fonll_mismatched(self):
    #     kernels = []

    #     for k in self.collect_fonll():
    #         k.max_order = evolution_pto
    #         kernels.append(k)

    #     for k in self.collect_ffns():
    #         k.min_order = evolution_pto
    #         kernels.append(k)

    #     return kernels

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
