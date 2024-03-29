import numpy as np

from .utils import dump_polarized as dump

# renaming
new_names = {
    "athena_29gev_ep": ["ATHENA_NC_29GEV_EP_G1", "ATHENA_NC_29GEV_EP_F1"],
    "athena_45gev_ep": ["ATHENA_NC_45GEV_EP_G1", "ATHENA_NC_45GEV_EP_F1"],
    "athena_63gev_ep": ["ATHENA_NC_63GEV_EP_G1", "ATHENA_NC_63GEV_EP_F1"],
    "athena_105gev_ep": ["ATHENA_NC_105GEV_EP_G1", "ATHENA_NC_105GEV_EP_F1"],
    "athena_140gev_ep": ["ATHENA_NC_140GEV_EP_G1", "ATHENA_NC_140GEV_EP_F1"],
}
