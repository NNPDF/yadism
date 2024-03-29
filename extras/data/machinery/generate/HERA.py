from .utils import load, obs_template


def dump(path, _target):
    if path.parent.stem == "HERACOMB":
        return dump_HERACOMB(path)
    if path.parent.stem in ["HERACOMB_SIGMARED_C", "HERACOMB_SIGMARED_B"]:
        return dump_HERACOMB_heavy(path)
    else:
        raise ValueError("HERA set not recognized")


def dump_HERACOMB(src_path):
    """
    Write HERACOMB observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    esf = load(src_path, 2, ["Q2", "x", "y"])
    is_cc = "CC" in src_path.stem
    obs["prDIS"] = "CC" if is_cc else "NC"
    xs = "XSHERACC" if is_cc else "XSHERANC"
    obs["observables"] = {xs: esf}
    obs["ProjectileDIS"] = "electron" if "EM" in src_path.stem else "positron"

    return obs


def dump_HERACOMB_heavy(src_path):
    """
    Write HERACOMB heavy observables.

    Parameters
    ----------
        src_path : str
            input path
        target_path : str
            target path
    """
    obs = obs_template.copy()
    raw_esfs = load(src_path, 36, ["Q2", "x"])
    # y has to be computed instead - see DataInfo on the respective file
    esfs = []
    for raw_esf in raw_esfs:
        raw_esf.update({"y": raw_esf["Q2"] / 318.0**2 / raw_esf["x"]})
        esfs.append(raw_esf)

    obs["prDIS"] = "NC"
    xs = "XSHERANCAVG"
    if "Charm" in str(src_path):
        xs += "_charm"
    elif "Beauty" in str(src_path):
        xs += "_bottom"
    obs["observables"] = {xs: esfs}
    obs["ProjectileDIS"] = "electron"

    return obs


# renaming
new_names = {
    "HERACOMBCCEM": "HERA_CC_318GEV_EM_SIGMARED",
    "HERACOMBCCEP": "HERA_CC_318GEV_EP_SIGMARED",
    "HERACOMBNCEM": "HERA_NC_318GEV_EM_SIGMARED",
    "HERACOMBNCEP460": "HERA_NC_225GEV_EP_SIGMARED",
    "HERACOMBNCEP575": "HERA_NC_251GEV_EP_SIGMARED",
    "HERACOMBNCEP820": "HERA_NC_300GEV_EP_SIGMARED",
    "HERACOMBNCEP920": "HERA_NC_318GEV_EP_SIGMARED",
    "d18-037.tableCharm": "HERA_NC_318GEV_EAVG_SIGMARED_CHARM",
    "d18-037.tableBeauty": "HERA_NC_318GEV_EAVG_SIGMARED_BOTTOM",
}
