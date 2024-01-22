"""Collect all kernels for given |FNS|."""
import numpy as np
from eko.matchings import nf_default

from . import asy, heavy, intrinsic, kernels, light
from .partonic_channel import EmptyPartonicChannel


class Component(list):
    """Used for organize elements and debugging purpose."""

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
    """Does the matching between coefficient functions and partons with their appropriate coupling strength.

    Parameters
    ----------
    esf : EvaluatedStructureFunction
        current ESF

    """

    def __init__(self, esf):
        self.esf = esf
        self.masses = {4 + i: not mass for i, mass in enumerate(esf.info.ZMq)}
        self.intrinsic = esf.info.intrinsic_range
        self.obs_name = esf.info.obs_name
        self.nf = nf_default(esf.Q2, esf.info.threshold)
        self.target = esf.info.target
        self.scheme = esf.info.scheme
        self.fonllparts = esf.info.fonllparts

    def collect(self):
        """Collect all kernels."""
        comps = []
        family = self.obs_name.flavor_family
        # Adding light component
        if family in ["light", "total"] and self.fonllparts in ["massless", "full"]:
            comps.append(self.light_component())
        if family == "heavy" and self.fonllparts in ["massless", "full"]:
            # the only case in which an heavy contribution is not present in those
            # accounted for in total, it's when heavy already became heavylight
            comps.extend(self.heavylight_components())
        if family in ["heavy", "total"] and self.fonllparts in ["massive", "full"]:
            comps.extend(self.heavy_components())
        return comps

    def light_component(self):
        """Collect massless kernels."""
        nf = self.nf
        masses = self.masses

        comp = Component(0)
        # light does not contain any mass effects and so is just always there
        comp.extend(light.kernels.generate(self.esf, nf))
        # instead missing encodes mass effects and so we need to fork:
        for ihq in range(nf + 1, 7):
            if masses[ihq]:
                if "FFN0" in self.scheme:
                    comp.extend(
                        asy.kernels.generate_missing_asy(
                            self.esf,
                            nf,
                            ihq,
                            self.esf.info.theory["pto_evol"],
                        )
                    )
                else:
                    comp.extend(heavy.kernels.generate_missing(self.esf, nf, ihq))

        return comp

    def heavylight_components(self):
        """Collect single-flavor massless kernels."""
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
        """Collect massive kernels."""
        nf = self.nf
        hq = self.obs_name.hqnumber
        masses = self.masses

        comps = []

        heavy_comps = {}
        # The loop starts at nf because nf counts the number of quarks of which
        # are above the mass threshold. For these quarks the masses are not
        # considered.
        for sfh in range(nf, 7):
            # exclude sfh=3, since heavy contributions are there for [4,5,6]
            # if it's ZM you don't even have the component
            if sfh not in masses:
                continue

            # There is no massive heavy contribution for ZM
            if not masses[sfh]:
                continue

            heavy_comps[sfh] = Component(sfh)

            # calculate only the contribution corresponding to the observable
            # i.e. charm for F_charm, bottom for F_bottom. In the case of
            # F_total (if hq=0), sum over all massive contributions.
            if hq not in (0, sfh):
                continue

            if sfh in self.intrinsic:  # heavy quark is intrinsic
                if "FFN0" in self.scheme:
                    heavy_comps[sfh].extend(
                        asy.kernels.generate_intrinsic_asy(
                            self.esf, nf, self.esf.info.theory["pto_evol"], ihq=sfh
                        ),
                    )
                else:
                    heavy_comps[sfh].extend(
                        intrinsic.kernels.generate(self.esf, ihq=sfh)
                    )

            if "FFN0" in self.scheme:
                heavy_comps[sfh].extend(
                    asy.kernels.generate_heavy_asy(
                        self.esf, nf, self.esf.info.theory["pto_evol"], ihq=sfh
                    )
                )
            else:
                heavy_comps[sfh].extend(heavy.kernels.generate(self.esf, nf, ihq=sfh))

            comps.append(heavy_comps[sfh])
        return comps

    @staticmethod
    def apply_isospin(full, z, a):
        """Apply isospin symmetry to u and d distributions.

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
        """Drop kernels with :class:`EmptyPartonicChannel` or its partons with empty weight.

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
        """Collect all kernels according to the |FNS|.

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
