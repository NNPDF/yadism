# -*- coding: utf-8 -*-
# pylint: skip-file
# fmt: off
# Our testing playground
import copy
import pathlib
import subprocess

import lhapdf
import numpy as np
import yaml
from banana.data import cartesian_product
from yadmark.benchmark.runner import Runner
from yadmark.data import observables

here = pathlib.Path(__file__).parent

lhapdf.pathsPrepend(subprocess.run("lhapdf-config --datadir".split(), capture_output=True).stdout.decode().strip())

class Sandbox(Runner):

    # external comparison program
    external = "APFEL"
    #external = "xspace_bench"
    #external = "QCDNUM"
    #external = "void"

    # alphas_from_lhapdf = True

    @staticmethod
    def generate_observables():
        defaults = copy.deepcopy(observables.default_card)
        xgrid = np.array(defaults["interpolation_xgrid"]).copy()
        #interpolation_xgrid = np.linspace(1e-1, 1, 9).tolist()
        kinematics = []
        # kinematics.extend([dict(x=x, Q2=20.0) for x in xgrid[:-1:5]])
        kinematics.extend([dict(x=x, Q2=20.0, y=0) for x in np.geomspace(1e-4, .9, 10)])
        kinematics.extend([dict(x=x, Q2=2, y=0) for x in np.geomspace(1e-4, .9, 10)])
        #kinematics.extend([dict(x=x, Q2=2**2, y=0) for x in np.geomspace(2e-5, 1e-2, 10)])
        #kinematics.extend([dict(x=x, Q2=2, y=0) for x in np.geomspace(2e-5, 1e-2, 10)])
        # kinematics.extend([dict(x=.01, Q2=10, y=y) for y in np.linspace(0, .9, 10)])
        # kinematics.extend([dict(x=x, Q2=90) for x in np.linspace(.8, .99, 10).tolist()])
        # kinematics.extend([dict(x=0.10914375746330703, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
        # kinematics.extend([dict(x=0.0051, Q2=Q2) for Q2 in np.geomspace(10, 1e5, 60).tolist()])
        # kinematics = [dict(x=0.001,Q2=1e4)]
        # kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.geomspace(500, 800, 10).tolist()])
        kinematics.extend([dict(x=0.1, Q2=Q2,y=0) for Q2 in np.linspace(2, 50, 10).tolist()])
        kinematics.extend([dict(x=0.001, Q2=Q2,y=0) for Q2 in np.linspace(2, 50, 10).tolist()])
        # kinematics.extend([dict(x=x, Q2=30.0, y=0) for x in np.geomspace(1e-4, .9, 10)])
        # kinematics.extend([dict(x=x, Q2=4**2, y=0) for x in np.geomspace(1e-4, .9, 10)])
        # kinematics.extend([dict(x=0.1, Q2=Q2,y=0) for Q2 in np.geomspace(4**2, 1e2, 10).tolist()])
        # kinematics.extend([dict(x=0.001, Q2=Q2,y=0) for Q2 in np.geomspace(4**2, 1e2, 10).tolist()])

        observable_names = [
            # "F2_light",
            # "FL_light",
            # "F3_light",
            #"F2_charm",
            # "FL_charm",
            # "F3_charm",
            # "F2_bottom",
            # "F2_top",
            # "FL_bottom",
            # "F3_bottom",
            "F2_total",
            # "FL_total",
            # "F3_total",
            #  "XSHERANC",
            # "XSHERACC_light",
            # "XSHERACC_charm",
            #"XSHERANC",
            #"XSHERACC",
            #"XSCHORUSCC_light",
            #"XSCHORUSCC_charm",
            #"XSCHORUSCC",
            #"XSNUTEVCC_charm"
        ]
        #update = {"prDIS": ["EM"],"interpolation_xgrid":[interpolation_xgrid], "interpolation_polynomial_degree": [4]}
        update = {"prDIS": ["NC"], "ProjectileDIS": ["electron"]}
        #update = {"prDIS": ["CC"], "ProjectileDIS": ["electron"]}
        #update = {"prDIS": ["EM"], "ProjectileDIS": ["electron"], "TargetDIS":["lead"]}
        #update= {}
        # card["PropagatorCorrection"] = .999
        # card["ProjectileDIS"] = "antineutrino"
        # card["PolarizationDIS"] = 0.5
        return observables.build(observable_names=observable_names,kinematics=kinematics,update=update)

    def doit(self):
        self.run([
                #{"PTO": 2, "NfFF": 5, "mc":2, "mb":3, "mt":4},
                #{"PTO": 0, "FNS": "FFNS", "mc": 1.95, "mb": 1e6, "mt": 1e8, "NfFF": 3},
                #{"PTO": 1, "FNS": "FFNS", "mc": 1.95, "mb": 1e6, "mt": 1e8, "NfFF": 3},
                #{"PTO": 2, "FNS": "FFNS", "mc": 1.95, "mb": 1e6, "mt": 1e8, "NfFF": 3},
                #{"PTO": 2, "FNS": "FONLL-C","NfFF":4,"IC":1,"mc":1.51,"Qmc":1.51,"mb":1e6,"mt":1e7,"ModEv":"TRN","MaxNfPdf":5,"MaxNfAs": 5, "Qmb":4.92,"Qmt":172.5,"alphas":0.118,"alphaqed":0.007496252,"Q0":1.65},
                #{"PTO": 1, "FNS": "FONLL-A", "mc": 1.95, "mb": 1e6,"mt": 1e8, "NfFF": 4},
                {"PTO": 1, "FNS": "FONLL-A", "mc": 1.51, "NfFF": 4},
                #{"PTO": 2, "FNS": "FONLL-B", "mc": 1.95, "mb": 1e6,"mt": 1e8, "NfFF": 4},
                #{"PTO": 2, "FNS": "FONLL-C", "mc": 1.95, "mb": 1e6,"mt": 1e8, "NfFF": 4},
                #{"PTO": 2, "FNS": "FONLL-C", "mc": 1.51, "mb": 1e6,"mt": 1e8, "NfFF": 4},
                #{"PTO": 2, "XIF": 1, "XIR": 1, "mb": 4.9913},
                #{"PTO": 2, "XIF": 2, "XIR": 2, "mb": 4.9915},
                #{"PTO": 2, "XIF": 1, "XIR": 1e5, "mb": 4.9909},
                #{"PTO": 1, "IC": 1, "FNS": "FONLL-A", "NfFF": 4, "mc": 1.51, "mb": 1e6, "mt": 1e8},
                #{"PTO": 1, "IC": 1, "FNS": "FFNS", "NfFF": 3, "mc": 1.51, "XIF": 1, "XIR": 1},
                #{"PTO": 1, "IC": 1, "FNS": "FFNS", "NfFF": 3, "mc": 1.51, "XIF": 2, "XIR": 1},
                #  {"PTO": 1, "FNS": "ZM-VFNS", "mc": 1e-2, "mb": 1e8, "mt": 1e9, "NfFF": 4},
            ], self.generate_observables(), [
                # "uonly",
                # "ubaronly",
                # "dbaronly",
                #"conly",
                #"toygonly",
                #"toyuonly",
                #"toyantichsing",
                #"toyt3only",
                #"conly",
                #"ToyLH",
                #"gonly",
                "NNPDF31_nnlo_as_0118",
                # "NN31g",
                # "NN31u",
                # "NN31c",
            ])

    def run_pineappl(self):
        import pineappl
        path = here / ".." / "data" / "200-HERA_NC_318GEV_EAVG_SIGMARED_CHARM.pineappl.lz4"
        cuts = slice(27,50)
        if not path.exists():
            raise FileNotFoundError(f"PineAPPL file {path} not found!")
        g = pineappl.grid.Grid.read(str(path))
        r = g.key_values()["runcard"]
        runcard = yaml.safe_load(r)
        t = runcard["theory"]
        o = runcard["observables"]
        for obs, kins in o["observables"].items():
            for kin in kins:
                for k,v in kin.items():
                    kin[k] = float(v)
            o["observables"][obs] = kins[cuts]
            #print(kins)
        o["observables"]["XSHERANCAVG_bottom"] = o["observables"]["XSHERANCAVG_charm"]
        del o["observables"]["XSHERANCAVG_charm"]
        t["TMC"] = 0
        t["FNS"] = "FONLL-A"
        #t["FNS"] = "FFNS"
        t["NfFF"] = 4
        t["PTO"] = 1
        #t["kDISbThr"] = 10
        #t["mb"] = 1e6
        #t["mt"] = 1e7
        self.run([t], [o],[
            "NNPDF31_nnlo_as_0118",
            "NN31g",
            "NN31u",
            "NN31c",
        ])

def main():
    sand = Sandbox()
    sand.doit()
    #sand.run_pineappl()

if __name__ == "__main__":
    main()
