# -*- coding: utf-8 -*-
import numpy as np

from . import fonll, heavy, intrinsic, light
from .partonic_channel import EmptyPartonicChannel


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
        self.obs_name = esf.sf.obs_name
        self.nf = esf.sf.threshold.nf(
            esf.Q2
        )  # TODO decide whether Q2 or muF2 is the correct thing
        self.target = esf.sf.target

    def collect_ffns(self):
        """
        Collects all kernels in the |FFNS|.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants
        """
        elems = []
        # light is *everything* up to nf and not only u+d+s
        if self.obs_name.flavor in ["light", "total"]:
            elems.extend(light.kernels.generate(self.esf, self.nf))
        if self.obs_name.flavor_family in ["heavy", "total"]:
            # there is only *one* finite mass available, i.e. the next one
            if (
                self.obs_name.flavor_family == "heavy"
                and self.obs_name.hqnumber != self.nf + 1
            ):
                raise ValueError(
                    f"{self.obs_name} is not available in FFNS with nl={self.nf}"
                )
            elems.extend(heavy.kernels.generate(self.esf, self.nf))
            ihq = self.nf + 1
            if ihq in self.esf.sf.intrinsic_range:
                elems.extend(intrinsic.kernels.generate(self.esf, ihq))
        return elems

    def collect_zmvfns(self):
        """
        Collects all kernels for |ZM-VFNS|.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants
        """
        elems = []
        # light is *everything* up to nf and not only u+d+s
        if self.obs_name.flavor in ["light", "total"]:
            elems.extend(light.kernels.generate(self.esf, self.nf))
        # heavy is not allowed
        if self.obs_name.flavor_family in ["heavy"]:
            raise ValueError(f"{self.obs_name} is not available in ZM-VFNS")
        return elems

    def collect_fonll(self):
        """
        Collects all kernels for FONLL.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants
        """
        elems = []
        # above the *next* threshold use ZM-VFNS
        nl = self.esf.sf.nf_ff - 1
        if nl + 1 < self.nf:
            return self.collect_zmvfns()

        if self.obs_name.flavor in ["light", "total"]:
            elems.extend(light.kernels.generate(self.esf, nl))
            # add F^d
            elems.extend(
                self.damp_elems(nl, fonll.kernels.generate_light_diff(self.esf, nl))
            )
        if self.obs_name.flavor_family in ["heavy", "total"]:
            elems.extend(heavy.kernels.generate(self.esf, nl))
            # add F^d
            ihq = nl + 1
            if ihq in self.esf.sf.intrinsic_range:
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
        if not self.esf.sf.FONLL_damping:
            return elems
        nhq = nl + 1
        m2hq = self.esf.sf.m2hq[nhq - 4]
        power = self.esf.sf.damping_powers[nhq - 4]
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
        if self.esf.sf.scheme == "FFNS":
            full = self.collect_ffns()
        elif self.esf.sf.scheme == "ZM-VFNS":
            full = self.collect_zmvfns()
        elif self.esf.sf.scheme in ["FONLL-A"]:
            full = self.collect_fonll()
        else:
            raise ValueError("Unknown FNS")

        # add level-0 nuclear correction: apply isospin symmetry
        self.apply_isospin(full, self.target["Z"], self.target["A"])

        # drop all kernels with 0 weight, or empty coeffs
        return self.drop_empty(full)
