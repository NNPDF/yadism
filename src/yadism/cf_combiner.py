# -*- coding: utf-8 -*-
"""
F2total in ZM-VFNS
[{
    couplings: {1: 1/9, 2: 4/9},
    coeff: F2lightNonSinglet
},
]

F2charm in FONLL in EM:
[{ # eq. 90
    couplings: {21: 1},
    coeff: F2heavyGluonVV(Q2, nf=nl,m=mc)
},{
    couplings: {1: 1, 2: 1, 3: 1, -1: 1, -2: 1, -3: 1},
    coeff: F2heavySingletVV(Q2, nf=nl,m=mc)
}, { # eq. 91
    couplings: {21: -1},
    coeff: F2asyGluonVV(Q2, nf=nl,m=mc)
},{
    couplings: {1: 1, 2: 1, 3: 1, -1: 1, -2: 1, -3: 1},
    coeff: F2AsySingletVV(Q2, nf=nl,m=mc)
}, { # eq. 92
    couplings: {1: 1/9, 2: 4/9, 3: 1/9, 4: 4/9, ...},
    coeff: F2lightNonSinglet(nf=nl+1)
}, {
    couplings: {1: 1/9, 2: 4/9, 3: 1/9, 4: 4/9, ...},
    coeff: F2lightSinglet(nf=nl+1)
}, {
    couplings: {21: 1},
    coeff: F2lightGluon(nf=nl+1)
}
]

"""

from .nc import kernels as nc_kernels
from .cc import kernels as cc_kernels


class CoefficientFunctionsCombiner:
    """
    Do the matching between coefficient functions and partons with their approptiate coupling
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
        Collect the coefficient functions in the FFNS

        Returns
        -------
            elems : list(dict)
                all participants
        """
        elems = []
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

    def collect_fonll(self):
        if self.obs_name.flavor_family in ["heavy", "total"]:
            pass

    def collect_elems(self):
        if self.esf.sf.threshold.scheme == "FFNS":
            full = self.collect_ffns()
        # drop all elements that have 0 weight
        return full
