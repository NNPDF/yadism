# -*- coding: utf-8 -*-

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
        self.nf = esf.sf.threshold.get_areas(esf.Q2 * esf.sf.xiF ** 2)[-1].nf

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
            raise ValueError(
                f"{self.obs_name} is not available in ZM-VFNS"
            )
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
        if self.obs_name.flavor_family in ["heavy", "total"]:
            pass
        return elems

    def collect_elems(self):
        """
        Collects all kernels according to the |FNS|.

        Returns
        -------
            elems : list(yadism.kernels.Kernel)
                all participants
        """
        if self.esf.sf.threshold.scheme == "FFNS":
            full = self.collect_ffns()
        elif self.esf.sf.threshold.scheme == "ZM-VFNS":
            full = self.collect_zmvfns()
        # drop all elements that have 0 weight
        return full
