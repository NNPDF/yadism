# Testing the loading functions
from yadism.runner import run_dis

def test_loader():
    """Test the loading mechanism"""

    # Allocate a theory from NNPDF database at LO (theory.ID = 52)
    theory = {
        'ID': 52,
        'PTO': 1,
        'FNS': 'FONLL-B',
        'DAMP': 0,
        'IC': 1,
        'ModEv': 'TRN',
        'XIR': 1.0,
        'XIF': 1.0,
        'NfFF': 5,
        'MaxNfAs': 5,
        'MaxNfPdf': 5,
        'Q0': 1.65,
        'alphas': 0.118,
        'Qref': 91.2,
        'QED': 0,
        'alphaqed': 0.007496252,
        'Qedref': 1.777,
        'SxRes': 0,
        'SxOrd': 'LL',
        'HQ': 'POLE',
        'mc': 1.51,
        'Qmc': 1.51,
        'kcThr': 1.0,
        'mb': 4.92,
        'Qmb': 4.92,
        'kbThr': 1.0,
        'mt': 172.5,
        'Qmt': 172.5,
        'ktThr': 1.0,
        'CKM': '0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152',
        'MZ': 91.1876,
        'MW': 80.398,
        'GF': 1.1663787e-05,
        'SIN2TW': 0.23126,
        'TMC': 1,
        'MP': 0.938,
        'Comments': 'NNPDF3.1 NLO central',
        'global_nx': 0,
        'EScaleVar': 1.
    }

    process = {
        'process': 'F2',
        'x': 0.1,
        'Q2': 90
    }

    test_dict = {**theory, **process}

    # esecute DIS
    result = run_dis(test_dict)

    assert(result["F2"] == 0)
