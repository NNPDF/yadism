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

from . import nc
from . import cc


class CoefficientFunctionElement:
    def __init__(self, partons, coeff):
        self.partons = partons
        self.coeff = coeff


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
        self.process = esf.sf.obs_params["process"]
        self.nf = esf.sf.threshold.get_areas(esf.Q2 * esf.sf.xiF ** 2)[-1].nf
        self.cfs = self.select_coefficient_functions(self.process, self.obs_name.kind)

    def generate_light(self, nf):
        """
        Collect the light coefficient functions

        Parameters
        ----------
            nf : int
                number of light flavors

        Returns
        -------
            elems : list(CoefficientFunctionElement)
                list of elements
        """
        # quark couplings
        tot_ch_sq = 0
        ns_partons = {}
        pids = range(1, nf + 1)
        for q in pids:
            w = self.esf.sf.coupling_constants.get_weight(
                q, self.esf.Q2, self.obs_name.kind
            )
            ns_partons[q] = w
            ns_partons[-q] = w if self.obs_name.kind != "F3" else -w
            tot_ch_sq += w
        ns = CoefficientFunctionElement(
            ns_partons, self.cfs["light"]["ns"](self.esf, nf=nf)
        )
        # gluon coupling = charge average (omitting the *2/2)
        ch_av = tot_ch_sq / len(pids)
        g = CoefficientFunctionElement(
            {21: ch_av}, self.cfs["light"]["g"](self.esf, nf=nf)
        )
        # same for singlet
        s_partons = {q: ch_av for q in ns_partons}
        s = CoefficientFunctionElement(
            s_partons, self.cfs["light"]["s"](self.esf, nf=nf)
        )
        return (ns, g, s)

    @staticmethod
    def select_coefficient_functions(dis_currrent, kind):
        """
        Collect all necessary coefficient functions

        Parameters
        ----------
            dis_current : str
                exchanged electro-weak boson
            kind : str
                structure function

        Returns
        -------
            cfs : dict
                mapping of coefficient functions
        """
        if dis_currrent == "CC":
            cfs = cc.coefficient_functions
        else:
            cfs = nc.coefficient_functions
        return cfs[kind]

    def collect_ffns(self):
        """
        Collect the coefficient functions in the FFNS

        Returns
        -------
            elems : list(dict)
                all participants
        """
        elems = []
        # light is trivial
        if self.obs_name.flavor in ["light", "total"]:
            elems.extend(self.generate_light(self.nf))
        # add heavy
        if self.obs_name.flavor_family in ["heavy", "total"]:
            # there is only *one* finite mass available, i.e. the next one
            if (
                self.obs_name.flavor_family == "heavy"
                and self.obs_name.hqnumber != self.nf + 1
            ):
                raise ValueError(
                    f"{self.obs_name} is not available in FFNS with nl={self.nf}"
                )
            nhq = self.nf + 1  # this way it will also work for total
            m2hq = self.esf.sf.m2hq[nhq - 4]
            # add contributions
            weight_vv = self.esf.sf.coupling_constants.get_weight(
                nhq, self.esf.Q2, self.obs_name.kind, "V"
            )
            weight_aa = self.esf.sf.coupling_constants.get_weight(
                nhq, self.esf.Q2, self.obs_name.kind, "A"
            )
            gVV = CoefficientFunctionElement(
                {21: weight_vv}, self.cfs["heavy"]["gVV"](self.esf, m2hq=m2hq)
            )
            gAA = CoefficientFunctionElement(
                {21: weight_aa}, self.cfs["heavy"]["gAA"](self.esf, m2hq=m2hq)
            )
            # if self.obs_name.flavor == "bottom":
            # import pdb; pdb.set_trace()
            elems.extend((gVV, gAA))
        return elems

    def collect_fonll(self):
        if self.obs_name.flavor_family in ["heavy", "total"]:
            pass

    def collect_elems(self):
        if self.esf.sf.threshold.scheme == "FFNS":
            full = self.collect_ffns()
        # drop all elements that have 0 weight
        return full
