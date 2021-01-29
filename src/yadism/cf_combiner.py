# -*- coding: utf-8 -*-
import numpy as np

from .nc import kernels as nc_kernels
from .cc import kernels as cc_kernels


class CoefficientFunctionsCombiner:
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
        if esf.sf.obs_params["process"] == "CC":
            self.kernels = cc_kernels
        else:
            self.kernels = nc_kernels
        self.nf = esf.sf.threshold.nf(
            esf.Q2 * esf.sf.xiF ** 2
        )  # TODO decide whether Q2 or muF2 is the correct thing

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
            elems.extend(self.kernels.generate_light(self.esf, self.nf))
        if self.obs_name.flavor_family in ["heavy", "total"]:
            # there is only *one* finite mass available, i.e. the next one
            if (
                self.obs_name.flavor_family == "heavy"
                and self.obs_name.hqnumber != self.nf + 1
            ):
                raise ValueError(
                    f"{self.obs_name} is not available in FFNS with nl={self.nf}"
                )
            elems.extend(self.kernels.generate_heavy(self.esf, self.nf))
            ihq = self.nf + 1
            if ihq in self.esf.sf.intrinsic_range:
                elems.extend(self.kernels.generate_intrinsic(self.esf, ihq))
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
            elems.extend(self.kernels.generate_light(self.esf, self.nf))
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
            elems.extend(self.kernels.generate_light(self.esf, nl))
            # add F^d
            elems.extend(
                self.damp_elems(
                    nl, self.kernels.generate_light_fonll_diff(self.esf, nl)
                )
            )
        if self.obs_name.flavor_family in ["heavy", "total"]:
            elems.extend(self.kernels.generate_heavy(self.esf, nl))
            # add F^d
            elems.extend(
                self.damp_elems(
                    nl, self.kernels.generate_heavy_fonll_diff(self.esf, nl)
                )
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
        power = self.esf.sf.damping_powers[nhq - 3]
        if self.esf.Q2 > m2hq:
            damp = np.power(1.0 - m2hq / self.esf.Q2, power)
        else:
            damp = 0.0
        return (damp * e for e in elems)

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
        # TODO drop all elements that have 0 weight
        return full
