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

class CoefficientFunctionsCombiner():

    def __init__(self, esf):
        self.esf = esf
        self.kind = esf.sf.obs_name.kind
        self.flavor = esf.sf.obs_name.flavor
        self.process = esf.sf.obs_params["process"]
        self.nf = esf.sf.threshold.get_areas(esf.Q2 * esf.sf.xiF ** 2)[-1].nf

    @staticmethod
    def select_coefficient_functions(dis_currrent, kind):
        if dis_currrent == "NC":
            cfs = nc.coefficient_functions
        else:
            cfs = cc.coefficient_functions
        return cfs[kind]

    def collect_ffns(self):
        cfs = self.select_coefficient_functions(self.process, self.kind)
        elems = []
        if self.flavor == "light":
            pass
        return elems

    def collect_elems(self):
        if self.esf.sf.threshold.scheme == "FFNS":
            full = self.collect_ffns()
        # drop all elements that have 0 weight
        #filter(full)
        return full
